from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Optional,Literal
from pydantic import BaseModel,Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
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
from IPython.display import display,Markdown
class InputState(TypedDict,total=False):
    user_query:str
    user_code:Optional[str]
    problem_id:Optional[int]

class OutputState(TypedDict):
    user_query:str
    user_code:Optional[str]
    problem_id:Optional[int]
    answer:str

class GraphState(TypedDict):
    user_query:str
    user_code:Optional[str]
    user_intent:str
    problem_id:Optional[int]
    answer:Optional[str]
    reasoning:str

build=StateGraph(GraphState,input_schema=InputState,output_schema=OutputState)

class ProblemMetadata:
    description:str
    title:str
    constraints:str
    difficulty:str
    time_limit_ms:str

# --- Intent Classification Schema ---
class UserIntent(BaseModel):
    """Classify the user's intent based on their query and code."""
    
    user_intent: Literal[
        "how_to_solve_this", 
        "why_my_code_failed", 
        "explain_my_code", 
        "validate_my_approach", 
        "clarification_request", 
        "general_dsa_concept", 
        "i_cant_answer_to_this"
    ] = Field(..., description="The classified intent of the user.")
    
    reasoning: str = Field(..., description="Brief reason why this intent was chosen.")

def query_intent(state: InputState) -> dict:
    structured_llm = llm.with_structured_output(UserIntent)
    
    user_query = state.get("user_query", "")
    user_code = state.get("user_code", None)

    system_prompt = """You are a highly specialized Competitive Programming (CP) Assistant. Your SOLE purpose is to assist with algorithmic problems (LeetCode, Codeforces, AtCoder) and Data Structures & Algorithms (DSA).

    You operate under a STRICT "White-list" policy. If a query does not fall into the specific domains of Algorithms, Data Structures, or Problem Solving logic, you MUST classify it as 'i_cant_answer_to_this'.

    Classify the user's intent into exactly one of these categories:

    1. 'how_to_solve_this': 
       - User asks for hints, approach, or strategy for a specific algorithmic problem.
       - Logic: "How do I approach this?", "Any hints for LeetCode 123?"

    2. 'why_my_code_failed': 
       - User provides code that is failing (WA/TLE/RE) on a judge and asks why.
       - Logic: MUST have user_code OR reference a verdict (e.g., "Getting TLE").

    3. 'explain_my_code': 
       - User asks to explain the logic, flow, or complexity of a provided code snippet.

    4. 'validate_my_approach': 
       - User proposes a specific algorithm/idea (e.g., "Greedy", "DP") and asks if it is valid for a problem.

    5. 'clarification_request': 
       - STRICTLY for doubts about a problem's constraints, input format, or edge cases.
       - Example: "Is N up to 10^5?", "Can the array be empty?"

    6. 'general_dsa_concept': 
       - Theoretical questions about DSA concepts (Sorting, Graphs, DP, Trees).
       - Example: "How does Dijkstra work?", "Time complexity of Merge Sort?"

    7. 'i_cant_answer_to_this': 
       - THE CATCH-ALL FOR EVERYTHING ELSE.
       - REJECT General Programming: "How to center a div?", "How to install React?", "pandas vs numpy?", "How to build an API?"
       - REJECT General Knowledge: History, politics, weather, sports, movies.
       - REJECT Casual Chat: "Hi", "How are you?", "Tell me a joke" (unless accompanied by a problem).
       - REJECT Homework/Math: "Solve this calculus integral", "Write an essay".
       
    *** IMPORTANT DECISION RULES ***
    - If the query is technical (e.g., "How to fix this CSS?") but NOT about Algorithms/DSA -> 'i_cant_answer_to_this'.
    - If the query is about a specific library/framework (React, Django, Spring, Pandas) -> 'i_cant_answer_to_this'.
    - If you are unsure if it relates to Competitive Programming, CHOOSE 'i_cant_answer_to_this'.
    """


    messages = [
        ("system", system_prompt),
        ("human", "User Query: {user_query}\n\nUser Code: {user_code}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chain = prompt | structured_llm
    
    result: UserIntent = chain.invoke({
        "user_query": user_query, 
        "user_code": "No code provided" if not user_code else user_code
    })

    return {
        "user_intent": result.user_intent,
        "user_query": user_query,
        "user_code": user_code,
        "problem_id": state.get("problem_id",None),
        "reasoning":result.reasoning
    }

def handle_how_to_solve_this(state: GraphState) -> GraphState:
    return {
        **state,
        "answer": "handle_how_to_solve_this"
    }


def handle_why_my_code_failed(state: GraphState) -> GraphState:
    return {
        **state,
        "answer": "handle_why_my_code_failed"
    }


def handle_explain_my_code(state: GraphState) -> GraphState:
    return {
        **state,
        "answer": "handle_explain_my_code"
    }


def handle_validate_my_approach(state: GraphState) -> GraphState:
    return {
        **state,
        "answer": "handle_validate_my_approach"
    }


def handle_general_dsa_concept(state: GraphState) -> OutputState:
    user_query = state.get("user_query", "")
    
    # Improved Prompt: Includes TL;DR at start and Summary at end
    prompt = ChatPromptTemplate.from_template(
        """You are an elite Competitive Programming Coach.
        The user wants a deep-dive explanation of the concept: "{user_query}"

        Your Goal: Provide a comprehensive, top-to-bottom guide suitable for a coder preparing for contests like Codeforces or LeetCode.

        Structure your response strictly as follows:

        ### 0. TL;DR
        - A 2-sentence high-level summary of what this algorithm/concept is and its primary use case. 
        - (Target audience: Experts who just need a refresher).

        ### 1. The "Big Idea" (Intuition)
        - Explain the concept simply without jargon first.
        - Use an analogy if helpful.
        - Why does this exist? What problem does it solve efficiently?

        ### 2. How It Works (The Algorithm)
        - Briefly describe the step-by-step logical flow.
        - Mention the underlying data structures used (e.g., "Uses a Min-Heap," "Relies on Recursion + Memoization").

        ### 3. Complexity Analysis
        - **Time Complexity**: Best, Average, and Worst case (with brief reasoning).
        - **Space Complexity**: Auxiliary space required.

        ### 4. Implementation Pattern (Python)
        - Provide a concise, standard "template" code snippet in Python.
        - Ensure the code is clean, commented, and follows standard CP practices.
        - DO NOT omit this section.

        ### 5. When to Use (Pattern Recognition)
        - List specific problem constraints or keywords that signal this approach (e.g., "N <= 10^5", "Shortest path with non-negative weights").

        ### 6. Common Pitfalls & Edge Cases
        - What usually breaks this algorithm? (e.g., "Integer overflow," "Negative cycles," "Recursion depth limit").

        ### 7. Summary
        - One final "Golden Rule" or key takeaway to remember about this concept during a contest.

        Keep the tone professional, encouraging, and highly technical.
        """
    )
    
    # Execute chain
    chain = prompt | llm
    response = chain.invoke({"user_query": user_query})
    
    return {
        "user_query": user_query,
        "user_code": state.get("user_code"),
        "problem_id": state.get("problem_id"),
        "answer": response.content
    }

def handle_clarification_request(state: GraphState) -> GraphState:
    return {
        **state,
        "answer": "handle_clarification_request"
    }


def handle_cant_answer(state: GraphState) -> OutputState:
    user_query = state.get("user_query", "")
    
    # 1. Strict refusal prompt
    prompt = ChatPromptTemplate.from_template(
        """You are a strict Competitive Programming Assistant (LeetCode/Codeforces expert).
        
        The user has asked a question that is OUT OF SCOPE for you: 
        "{user_query}"
        
        Your task:
        1. Politely decline to answer this specific question.
        2. Remind the user that you can only assist with Data Structures, Algorithms, and Coding Problems.
        3. Keep the response short (1-2 sentences).
        4. Do NOT attempt to answer the off-topic question even slightly.
        """
    )
    
    chain = prompt | llm
    response = chain.invoke({"user_query": user_query})
    
    return {
        "user_query": user_query,
        "user_code": state.get("user_code"),
        "problem_id": state.get("problem_id"),
        "answer": response.content 
    }


nodes_to_functions = [
    ("how_to_solve_this", handle_how_to_solve_this),
    ("why_my_code_failed", handle_why_my_code_failed),
    ("explain_my_code", handle_explain_my_code),
    ("validate_my_approach", handle_validate_my_approach),
    ("general_dsa_concept", handle_general_dsa_concept),
    ("clarification_request", handle_clarification_request),
    ("i_cant_answer_to_this", handle_cant_answer),
]
for node,function_name in nodes_to_functions:
    build.add_node(node,function_name)


build.add_node("query_intent",query_intent)
build.add_edge(START,"query_intent")
build.add_conditional_edges("query_intent",lambda x:x["user_intent"],{node:node for node,_ in nodes_to_functions})
for node,_ in nodes_to_functions:
    build.add_edge(node,END)

graph=build.compile()
# Does Dijkstra work with negative edges?
query="Does Dijkstra work with negative edges?"
# "Who found Djikstras algo? and explain the use cases of this algo"
response=graph.invoke({"user_query": query, "user_code": None})


answer=response["answer"]


display(Markdown(answer))