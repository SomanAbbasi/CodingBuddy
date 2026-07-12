from pathlib import Path

from langchain_core.tools import tool

PROJECT_ROOT = Path("generated_projects")


@tool
def write_file(project_name: str, filepath: str, content: str) -> str:
    """
    Create or overwrite a file inside the project folder.
    """

    folder = project_name.replace(" ", "_")

    full_path = PROJECT_ROOT / folder / filepath

    full_path.parent.mkdir(parents=True, exist_ok=True)

    full_path.write_text(content, encoding="utf-8")

    return f"Successfully wrote {full_path}"