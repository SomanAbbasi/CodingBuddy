

def planner_prompt(user_prompt: str) -> str:
    PLANNER_PROMPT = f"""
You are the PLANNER agent. Convert the user prompt into a COMPLETE engineering project plan.

User request:
{user_prompt}
    """
    return PLANNER_PROMPT




def architect_prompt(plan: str) -> str:
    return f"""
You are a software architect.

Generate an implementation plan for the following project.

Return ONLY implementation steps.

Each implementation step must have:

1. filepath
2. task_description

The task description should briefly describe what should be implemented in that file.

Project:

{plan}
"""
