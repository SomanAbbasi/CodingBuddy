from pydantic import BaseModel,Field


class File(BaseModel):
    path: str = Field(description="The path to the file to be created or modified")
    purpose: str = Field(description="The purpose of the file, e.g. 'main application logic', 'data processing module', etc.")


class Plan(BaseModel):
    name: str=Field(description="The name of the app to be built")
    description: str=Field(description="A brief description of the app to be built, e.g., 'A social media app for sharing photos and videos.'")
    techstack: str=Field(description="The technology stack to be used for building the app, e.g., 'React, Node.js, MongoDB, etc.'")
    features:list[str]=Field(description="A list of features to be included in the app, e.g., ['User authentication', 'Photo upload and sharing', 'Commenting and liking system', etc.]")
    files:list[str]=Field(description="A list of files to be generated for the app, e.g., ['index.html', 'app.js', 'style.css', etc.]")


