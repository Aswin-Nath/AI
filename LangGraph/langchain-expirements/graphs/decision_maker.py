from langgraph.graph import START,END,StateGraph
from langchain_core.messages import SystemMessage
from typing import TypedDict,Optional,Literal
from IPython.display import Markdown,display
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_KEY=os.getenv("GROQ_API_KEY")
# Initialize Groq LLM
model="llama-3.1-8b-instant"
llm = ChatGroq(
    api_key=GROQ_KEY,
    model_name=model,
    temperature=0
)


class InputState(TypedDict):
    question:str
class OutputState(TypedDict):
    answer:str
class GraphState(TypedDict):
    question:str
    answer:str

builder=StateGraph(GraphState,output_schema=OutputState,input_schema=InputState)

COMMON_APPROACH_PROMPT = """
You are a Data Structures and Algorithms tutor.

Given the problem below, explain the **core idea and intuition** behind solving it.
- Do NOT provide code.
- Do NOT assume a specific technique unless absolutely necessary.
- Focus on understanding the problem constraints and strategy.

Explain clearly and concisely.

Problem:
{question}
"""

DP_APPROACH_PROMPT = """
You are a DSA expert.

Explain how this problem can be solved using **Dynamic Programming**.

Your explanation must include:
1. Why DP is applicable
2. Definition of the DP state
3. Transition logic
4. Base cases
5. Time and space complexity

Do NOT write full code.
Use clear step-by-step reasoning.

Problem:
{question}
"""

GREEDY_APPROACH_PROMPT = """
You are a DSA expert.

Explain how this problem can be solved using a **Greedy approach**.

Your explanation must include:
1. The greedy choice being made
2. Why the greedy choice is optimal
3. Proof intuition or justification
4. Time and space complexity
5. Any edge cases or limitations

Do NOT write full code.
Be precise and rigorous.

Problem:
{question}
"""

def provide_common_approach(state: InputState) -> GraphState:
    resp = llm.invoke(
        COMMON_APPROACH_PROMPT.format(question=state["question"])
    )
    return {
        "question": state["question"],
        "answer": resp.content
    }

def provide_dp_approach(state: InputState) -> GraphState:
    resp = llm.invoke(
        DP_APPROACH_PROMPT.format(question=state["question"])
    )
    return {
        "question": state["question"],
        "answer": resp.content
    }

def provide_greedy_approach(state: InputState) -> GraphState:
    resp = llm.invoke(
        GREEDY_APPROACH_PROMPT.format(question=state["question"])
    )
    return {
        "question": state["question"],
        "answer": resp.content
    }

def find_problem_type(state: InputState):
    prompt = f"""
You are a STRICT algorithm classifier.

Your job is to decide whether Dynamic Programming (DP) is REQUIRED.

Return "dp" ONLY IF:
- The problem requires optimization (min/max/count/etc.), AND
- There are multiple competing choices, AND
- Overlapping subproblems must be combined to get the correct answer.

DO NOT return "dp" if:
- The problem can be solved by BFS or DFS,
- The problem is graph traversal (cycle detection, connectivity, reachability),
- A visited array or recursion stack is sufficient,
- The first valid traversal result is already correct.

IMPORTANT:
- Graph traversal problems are NOT DP.
- Storing a visited array does NOT make something DP.
- Memoization of visited states is NOT DP.

Allowed outputs (ONLY ONE WORD):
- dp
- greedy
- both
- not both

If DP is not REQUIRED, return "not both".

Problem:
{state["question"]}
"""



    llm_response = llm.invoke(prompt).content.strip().lower()
    print(llm_response)
    ans=[]
    if llm_response=="both":
        ans=["dp","greedy"]
    elif llm_response=="dp":
        ans=["dp"]
    elif llm_response=="greedy":
        ans=["greedy"]
    elif llm_response=="not both":
        ans=["common"]
    return ans
def entry_node(state:InputState)->InputState:
    return state
builder.add_node("find_problem_type",entry_node)
builder.add_node("dp_node",provide_dp_approach)
builder.add_node("greedy_node",provide_greedy_approach)
builder.add_node("common_node",provide_common_approach)

builder.add_edge(START,"find_problem_type")
builder.add_edge("dp_node",END)
builder.add_edge("greedy_node",END)
builder.add_edge("common_node",END)

builder.add_conditional_edges(
    "find_problem_type",
    find_problem_type,
    {
    "dp":"dp_node",
    "greedy":"greedy_node",
    "common":"common_node"
    }
    )
graph=builder.compile()

