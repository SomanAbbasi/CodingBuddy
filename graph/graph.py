

from dotenv import load_dotenv
from prompts import planner_prompt
from state import Plan,File

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph

load_dotenv()




llm=ChatGroq(model="qwen/qwen3.6-27b")




def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]
    res = llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )
    if res is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": res}



    
user_prompt="Create a Simple Todo List app"
prompt=planner_prompt(user_prompt)


res=llm.with_structured_output(Plan).invoke(planner_prompt(prompt))

print(res)

graph=StateGraph(dict)

graph.add_node("planner",planner_agent)

graph.set_entry_point("planner")

agent=graph.compile()



result=agent.invoke({"user_prompt": user_prompt})
print(result)
