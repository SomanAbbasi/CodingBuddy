def planner_prompt(user_prompt: str) -> str:
    return f"""You are the PLANNER agent for CodingBuddy.

Convert the user request into a complete, practical project plan.
List EVERY file the project needs (HTML, CSS, JS, README, etc.).
Keep the scope small enough to implement fully in one pass.

Respond with a valid JSON object matching the required schema.

User request:
{user_prompt}
"""


def architect_prompt(plan_json: str) -> str:
    return f"""You are a software architect for CodingBuddy.

Do NOT write code. Create one implementation step for EVERY file in the plan.
Each step must have clear implementation_notes so a coding agent can write the full file.

Cover all files listed in the plan. Do not skip any.

Respond with a valid JSON object matching the required schema.

Project plan (JSON):
{plan_json}
"""


def coder_prompt(
    project_name: str,
    task_json: str,
    planned_files: list[str],
    other_files: list[str],
) -> str:
    siblings = ", ".join(other_files) if other_files else "(none written yet)"
    all_files = ", ".join(planned_files)
    return f"""You are a senior software engineer for CodingBuddy.

Write the COMPLETE contents of exactly ONE file.
Respond with a valid JSON object with keys "filepath" and "content".
The "content" value must be the full source code as a JSON string (escape newlines properly).
No markdown fences. No explanations outside the JSON.

Project name: {project_name}
All project files: {all_files}
Already written: {siblings}

Rules:
- Produce production-ready, complete code for this single file only.
- If this is HTML, link external CSS/JS with <link> and <script src="..."> — do NOT inline CSS or JS when those files are in the project.
- Keep IDs, class names, and filenames consistent across the project.
- Use the exact filepath from the task.

Task (JSON):
{task_json}
"""
