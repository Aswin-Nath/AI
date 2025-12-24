from langgraph.graph import START,END,StateGraph
from Models.groq import llm
result=llm.invoke("who is current CM of kerala?")

print(result)
