import logging
import os
from typing import Literal

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph

from graph.prompts import architect_prompt, coder_prompt, planner_prompt
from graph.state import CoderState, GeneratedFile, ImplementationTask, Plan, TaskPlan
from graph.tools import write_project_file

load_dotenv()

logger = logging.getLogger(__name__)

# Free-tier Groq model (override with GROQ_MODEL in .env)
DEFAULT_MODEL = "llama-3.3-70b-versatile"


def build_llm() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Copy .env.example to .env and add your key "
            "from https://console.groq.com/keys"
        )

    model = os.getenv("GROQ_MODEL", DEFAULT_MODEL)
    return ChatGroq(
        model=model,
        temperature=0,
        max_tokens=8192,
        api_key=api_key,
    )


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def planner_agent(state: CoderState) -> dict:
    llm = build_llm()
    planner = llm.with_structured_output(Plan, method="json_schema")

    try:
        plan = planner.invoke(planner_prompt(state.user_prompt))
    except Exception as exc:
        logger.exception("Planner failed")
        return {"errors": [f"Planner error: {exc}"]}

    if not plan.files:
        return {"errors": ["Planner returned no files to create."]}

    logger.info("Plan ready: %s (%d files)", plan.name, len(plan.files))
    return {"plan": plan, "errors": []}


def architect_agent(state: CoderState) -> dict:
    if state.plan is None:
        return {"errors": ["Architect skipped: no plan available."]}

    llm = build_llm()
    architect = llm.with_structured_output(TaskPlan, method="json_schema")

    try:
        task_plan = architect.invoke(
            architect_prompt(state.plan.model_dump_json(indent=2))
        )
    except Exception as exc:
        logger.exception("Architect failed")
        return {"errors": [*(state.errors or []), f"Architect error: {exc}"]}

    if not task_plan.implementation_steps:
        return {
            "errors": [
                *(state.errors or []),
                "Architect returned no implementation steps.",
            ]
        }

    planned = {_normalize_path(f) for f in state.plan.files}
    covered = {
        _normalize_path(s.filepath) for s in task_plan.implementation_steps
    }
    for missing in sorted(planned - covered):
        task_plan.implementation_steps.append(
            ImplementationTask(
                filepath=missing,
                purpose=f"Implement {missing}",
                implementation_notes=(
                    f"Create a complete, working {missing} for the project "
                    f"'{state.plan.name}'. Integrate with the other project files."
                ),
            )
        )

    logger.info(
        "Architect ready: %d steps", len(task_plan.implementation_steps)
    )
    return {
        "task_plan": task_plan,
        "current_step_idx": 0,
        "generated_files": [],
    }


def coder_agent(state: CoderState) -> dict:
    if state.plan is None or state.task_plan is None:
        return {"errors": [*(state.errors or []), "Coder skipped: missing plan."]}

    steps = state.task_plan.implementation_steps
    if state.current_step_idx >= len(steps):
        return {}

    task = steps[state.current_step_idx]
    llm = build_llm()
    coder = llm.with_structured_output(GeneratedFile, method="json_schema")

    prompt = coder_prompt(
        project_name=state.plan.name,
        task_json=task.model_dump_json(indent=2),
        planned_files=state.plan.files,
        other_files=state.generated_files,
    )

    try:
        generated = coder.invoke(prompt)
    except Exception as exc:
        logger.exception("Coder failed on %s", task.filepath)
        return {
            "errors": [
                *(state.errors or []),
                f"Coder error for {task.filepath}: {exc}",
            ]
        }

    filepath = (generated.filepath or "").strip() or task.filepath
    content = generated.content
    if not content or not str(content).strip():
        return {
            "errors": [
                *(state.errors or []),
                f"Coder returned empty content for {filepath}",
            ]
        }

    try:
        written = write_project_file(state.plan.name, filepath, content)
    except Exception as exc:
        logger.exception("Write failed for %s", filepath)
        return {
            "errors": [
                *(state.errors or []),
                f"Write error for {filepath}: {exc}",
            ]
        }

    logger.info("Wrote %s", written)
    return {
        "generated_files": [*(state.generated_files or []), filepath],
        "current_step_idx": state.current_step_idx + 1,
    }


def after_planner(state: CoderState) -> Literal["architect", "__end__"]:
    if state.errors or state.plan is None:
        return END
    return "architect"


def after_architect(state: CoderState) -> Literal["coder", "__end__"]:
    if state.errors or state.task_plan is None:
        return END
    return "coder"


def should_continue(state: CoderState) -> Literal["coder", "__end__"]:
    if state.errors:
        return END
    if state.task_plan is None:
        return END
    if state.current_step_idx >= len(state.task_plan.implementation_steps):
        return END
    return "coder"


def build_graph():
    graph = StateGraph(CoderState)
    graph.add_node("planner", planner_agent)
    graph.add_node("architect", architect_agent)
    graph.add_node("coder", coder_agent)

    graph.set_entry_point("planner")
    graph.add_conditional_edges("planner", after_planner)
    graph.add_conditional_edges("architect", after_architect)
    graph.add_conditional_edges("coder", should_continue)

    return graph.compile()


agent = build_graph()
