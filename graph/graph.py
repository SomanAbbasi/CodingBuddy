from dotenv import load_dotenv
from prompts import planner_prompt, architect_prompt, coder_prompt
from state import Plan, TaskPlan, CoderState

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.graph import END

from tools import write_file

load_dotenv()


llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0,
)

llm_with_tools = llm.bind_tools([write_file])



def planner_agent(state: CoderState):
    user_prompt = state.user_prompt

    planner = llm.with_structured_output(
        Plan,
        method="json_schema",
    )

    plan = planner.invoke(planner_prompt(user_prompt))

    state.plan = plan
    return state



def architect_agent(state: CoderState):
    prompt = architect_prompt(
        state.plan.model_dump_json()
    )

    architect = llm.with_structured_output(
        TaskPlan,
        method="json_schema",
    )

    task_plan = architect.invoke(prompt)

    state.task_plan = task_plan
    state.current_step_idx = 0

    return state



def coder_agent(state: CoderState):

    task = state.task_plan.implementation_steps[
        state.current_step_idx
    ]

    prompt = coder_prompt(
        f"""
Project Name:
{state.plan.name}

Task:
{task.model_dump_json(indent=2)}
"""
    )

    response = llm_with_tools.invoke(prompt)

    state.messages = [response]

    return state

def next_file(state: CoderState):
    state.current_step_idx += 1
    return state


def should_continue(state: CoderState):

    if state.current_step_idx >= len(state.task_plan.implementation_steps):
        return END

    return "coder"



user_prompt = "Create a Simple Todo List app in html, css, javascript"

tool_node = ToolNode([write_file])

graph = StateGraph(CoderState)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)
graph.add_node("tools", tool_node)
graph.add_node("next_file", next_file)


graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_edge("coder", "tools")
graph.add_edge("tools", "next_file")
graph.add_conditional_edges(
    "next_file",
    should_continue,
)

graph.add_edge("tools", END)

graph.set_entry_point("planner")

agent = graph.compile()

result = agent.invoke(
    CoderState(
        user_prompt=user_prompt
    )
)

print(result)