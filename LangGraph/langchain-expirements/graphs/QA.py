from langgraph.graph import START,END,StateGraph
from langchain_core.messages import SystemMessage
from typing import TypedDict,Optional
from IPython.display import Markdown,display
from langchain_groq import ChatGroq
model="llama-3.1-8b-instant"
llm = ChatGroq(
    model_name=model,
    temperature=0
)

class GraphState(TypedDict):
    question:str
    answer:Optional[str]

builder=StateGraph(GraphState,total=False)

def explain_question(state:GraphState)->GraphState:
    llm_response=llm.invoke(state["question"])
    return {"question":state["question"],"answer":llm_response}

builder.add_node("explain_question",explain_question)
builder.add_edge(START,"explain_question")
builder.add_edge("explain_question",END)
graph=builder.compile()

