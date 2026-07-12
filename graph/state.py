from typing import Annotated, Optional

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class Plan(BaseModel):
    name: str = Field(description="Short project/app name")
    description: str = Field(description="Brief description of the app")
    techstack: str = Field(description="Technologies to use, e.g. HTML, CSS, JavaScript")
    features: list[str] = Field(description="Key features to implement")
    files: list[str] = Field(
        description="All files to create, e.g. ['index.html', 'style.css', 'script.js']"
    )


class ImplementationTask(BaseModel):
    filepath: str = Field(description="Relative file path to create, e.g. index.html")
    purpose: str = Field(description="Why this file exists")
    implementation_notes: str = Field(
        description="Detailed instructions for what code to write in this file"
    )


class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(
        description="One step per file, covering every file in the plan"
    )


class GeneratedFile(BaseModel):
    filepath: str = Field(description="Relative path of the file being written")
    content: str = Field(description="Full file contents — complete, runnable code")


class CoderState(BaseModel):
    user_prompt: str
    plan: Optional[Plan] = None
    task_plan: Optional[TaskPlan] = None
    current_step_idx: int = 0
    generated_files: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    messages: Annotated[list[AnyMessage], add_messages] = Field(default_factory=list)
