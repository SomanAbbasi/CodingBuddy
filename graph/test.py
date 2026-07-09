
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv()


class ImplementationTask(BaseModel):
    filepath: str = Field(description="The file path")
    task_description: str = Field(description="The task")


class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask]


llm = ChatGroq(model="qwen/qwen3.6-27b")

structured_llm = llm.with_structured_output(TaskPlan)

result = structured_llm.invoke(
    "Create exactly three implementation steps for a Todo application."
)

print(result)