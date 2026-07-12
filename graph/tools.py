from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent / "generated_projects"


def safe_project_folder(project_name: str) -> Path:
    folder = "".join(c if c.isalnum() or c in "-_" else "_" for c in project_name.strip())
    folder = folder.strip("_") or "untitled_project"
    return PROJECT_ROOT / folder


def write_project_file(project_name: str, filepath: str, content: str) -> str:
    """
    Create or overwrite a file inside the project folder.
    Rejects path traversal outside the project directory.
    """
    if not filepath or not filepath.strip():
        raise ValueError("filepath cannot be empty")

    project_dir = safe_project_folder(project_name).resolve()
    target = (project_dir / filepath).resolve()

    if not str(target).startswith(str(project_dir)):
        raise ValueError(f"Invalid filepath (path traversal blocked): {filepath}")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return str(target.relative_to(PROJECT_ROOT.parent))
