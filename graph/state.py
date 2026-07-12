
from pydantic import BaseModel, Field, ConfigDict

from typing import Optional, Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class File(BaseModel):
    path: str = Field(description="The path to the file to be created or modified")
    purpose: str = Field(description="The purpose of the file, e.g. 'main application logic', 'data processing module', etc.")


class Plan(BaseModel):
    name: str=Field(description="The name of the app to be built")
    description: str=Field(description="A brief description of the app to be built, e.g., 'A social media app for sharing photos and videos.'")
    techstack: str=Field(description="The technology stack to be used for building the app, e.g., 'React, Node.js, MongoDB, etc.'")
    features:list[str]=Field(description="A list of features to be included in the app, e.g., ['User authentication', 'Photo upload and sharing', 'Commenting and liking system', etc.]")
    files:list[str]=Field(description="A list of files to be generated for the app, e.g., ['index.html', 'app.js', 'style.css', etc.]")



class ImplementationTask(BaseModel):
    filepath: str = Field(
        description="File that this task belongs to"
    )

    purpose: str = Field(
        description="Why this file exists"
    )

    responsibilities: list[str] = Field(
        description="Main responsibilities of this file"
    )

    functions: list[str] = Field(
        description="Functions/classes/components that should be implemented"
    )

    dependencies: list[str] = Field(
        description="Other files this file depends on"
    )

    inputs: list[str] = Field(
        description="Inputs received"
    )

    outputs: list[str] = Field(
        description="Outputs produced"
    )

    implementation_notes: str = Field(
        description="Detailed instructions for the coding agent"
    )

class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(description="A list of steps to be taken to implement the task")
    model_config = ConfigDict(extra="allow")
    
class CoderState(BaseModel):
    user_prompt: str

    plan: Optional[Plan] = None

    task_plan: Optional[TaskPlan] = None

    messages: Annotated[list[AnyMessage], add_messages] = []

    current_step_idx: int = 0

    current_file_content: Optional[str] = None