


from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel,Field

load_dotenv()


class Plan(BaseModel):
    name: str=Field(description="The name of the app to be built")
    description: str=Field(description="A brief description of the app to be built, e.g., 'A social media app for sharing photos and videos.'")
    techstack: str=Field(description="The technology stack to be used for building the app, e.g., 'React, Node.js, MongoDB, etc.'")
    features:list[str]=Field(description="A list of features to be included in the app, e.g., ['User authentication', 'Photo upload and sharing', 'Commenting and liking system', etc.]")
    files:list[str]=Field(description="A list of files to be generated for the app, e.g., ['index.html', 'app.js', 'style.css', etc.]")


llm=ChatGroq(model="qwen/qwen3.6-27b")


res=llm.with_structured_output(Plan).invoke("Generate a plan for a Todo List app with the following specifications: The app should allow users to create, edit, and delete tasks. It should have a simple and intuitive user interface. The app should be built using React for the frontend and Node.js for the backend. The app should use MongoDB as the database to store tasks. The app should have user authentication to allow users to sign up and log in. The app should have a feature to mark tasks as completed and filter tasks based on their completion status.")

print(res)