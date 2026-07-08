


from langchain_groq import ChatGroq
from dotenv import load_dotenv

from prompts import planner_prompt
from state import Plan,File


load_dotenv()




llm=ChatGroq(model="qwen/qwen3.6-27b")


user_prompt="Create a Simple Todo List app"

prompt=planner_prompt(user_prompt)

res=llm.with_structured_output(Plan).invoke(planner_prompt(prompt))

print(res)