

def planner_prompt(user_prompt: str) -> str:
    PLANNER_PROMPT = f"""
You are the PLANNER agent. Convert the user prompt into a COMPLETE engineering project plan.

User request:
{user_prompt}
    """
    return PLANNER_PROMPT




def architect_prompt(plan: str):

    return f"""
You are an experienced software architect.

Your job is NOT to write code.

Your job is to prepare implementation tasks for another AI coding agent.

For EVERY file in the project create one implementation step.

Each implementation step MUST include

- filepath
- purpose
- responsibilities
- functions
- dependencies
- inputs
- outputs
- implementation_notes

The implementation_notes should clearly explain what should be written inside the file.

Project:

{plan}
"""