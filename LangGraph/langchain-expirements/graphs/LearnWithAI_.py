from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional, Literal
from pydantic import BaseModel, Field
from sqlalchemy.engine import URL
from sqlalchemy import create_engine, text
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

# ===============================
# 1. SETUP
# ===============================
GROQ_KEY = os.getenv("GROQ_API_KEY")
# Using a standard chat model setup
llm = ChatGroq(api_key=GROQ_KEY, model_name="llama-3.1-8b-instant", temperature=0)

url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="aswinnath@123",
    host="localhost",
    port=1024,
    database="ticket_raiser",
)
engine = create_engine(url)

def get_problem_by_id(problem_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, title, description FROM problems WHERE id = :pid"),
            {"pid": problem_id}
        )
        row = result.fetchone()
        if not row: return None
        return {"id": row.id, "title": row.title, "description": row.description}

# ===============================
# 2. STATE DEFINITIONS
# ===============================
class InputState(TypedDict):
    user_intent: Literal[
        "how_to_solve_this", "why_my_code_failed", "explain_my_code", 
        "validate_my_approach", "clarification_request"
    ]
    user_query: Optional[str]
    user_code: Optional[str]
    problem_id: int

class GraphState(TypedDict):
    user_intent: str
    user_query: str
    user_code: str
    problem_id: int
    problem: Optional[dict]
    answer: str
    is_valid: bool
    fallback_message: str
    violation_type: Literal[
        "solution_begging",
        "no_input",
        "off_topic",
        "wrong_button",
        "ambiguous",
        "ok"
    ]

class OutputState(TypedDict):
    answer: str

# Defined for the parser to know the schema
class GuardDecision(BaseModel):
    is_valid: bool = Field(..., description="true if valid, false if blocked")
    fallback_message: str = Field(..., description="Helpful message if blocked, empty string if valid")
    violation_type: Literal[
        "solution_begging",
        "no_input",
        "off_topic",
        "wrong_button",
        "ambiguous",
        "ok"
    ] = Field(default="ok", description="Type of violation for analytics")

# ===============================
# 3. SETUP NODE
# ===============================
def setup_node(state: InputState) -> GraphState:
    problem = get_problem_by_id(state["problem_id"])
    return {
        "user_intent": state["user_intent"],
        "user_query": state.get("user_query", "").strip(),
        "user_code": state.get("user_code", "").strip(),
        "problem_id": state["problem_id"],
        "problem": problem,
        "answer": "",
        "is_valid": True,
        "fallback_message": "",
        "violation_type": "ok"
    }

# ===============================
# 4. GLOBAL GUARDRAIL CONSTANTS
# ===============================
GLOBAL_OFF_TOPIC = (
    "I can only help with this coding problem. "
    "Please ask about the problem, your code, or your approach."
)

AMBIGUOUS_CLARIFY = (
    "Could you clarify what you mean? "
    "For example, are you asking about specific constraints, data properties, or guarantees?"
)

# ===============================
# 5. LLM GUARDRAILS (WITH STRICT FALLBACKS)
# ===============================
def run_guard_llm(system_prompt: str, user_input: str) -> dict:
    structured_llm = llm.with_structured_output(GuardDecision)
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", user_input)])
    try:
        result: GuardDecision = (prompt | structured_llm).invoke({})
        return {
            "is_valid": result.is_valid,
            "fallback_message": result.fallback_message,
            "violation_type": result.violation_type
        }
    except Exception:
        return {
            "is_valid": False,
            "fallback_message": "I couldn't interpret that clearly. Could you rephrase?",
            "violation_type": "ambiguous"
        }

def guard_how_to_solve(state: GraphState) -> GraphState:
    # FIRST: Check for empty/whitespace-only input
    if not state['user_query'] or not state['user_query'].strip():
        return {**state, "is_valid": False, "fallback_message": "Could you clarify what you'd like help with?", "violation_type": "no_input"}
    
    # Use LLM with lenient prompt - user already clicked Hint button, so assume good faith
    prompt = """
You are a lenient validator for "Get Hint" requests on a coding problem.

User already clicked the "Get Hint" button, so assume they want help understanding the problem/approach.

ACCEPT (is_valid=true) if user is asking about:
- Approach, strategy, or hints for solving
- How to think about the problem
- What concepts apply
- Any question about the problem or their thinking process

ONLY REJECT (is_valid=false) if user explicitly asks for:
- Complete solution code ("give me the code", "write the solution")
- Or completely off-topic garbage that has nothing to do with programming/this problem

Default: ACCEPT. Be generous. User clicked Hint button for a reason.

If INVALID:
- violation_type = "solution_begging" (if asking for code) or "off_topic" (if irrelevant)
- fallback_message = "I can only help with this coding problem. Please ask about the problem, your code, or your approach."

If VALID:
- is_valid = true
- fallback_message = ""
- violation_type = "ok"
"""

    res = run_guard_llm(prompt, f"Query: {state['user_query']}")
    return {**state, **res}

def guard_why_failed(state: GraphState) -> GraphState:
    # FIRST: Check if code is present and non-trivial
    code = state['user_code'].strip()
    
    if not code:
        return {**state, "is_valid": False, "fallback_message": "Please paste your code so I can help debug", "violation_type": "no_input"}
    
    # Check code substantiality: multiline counts as substantial, single line needs length >= 15
    lines = [l.strip() for l in code.split('\n') if l.strip() and not l.strip().startswith('#')]
    is_substantial = len(lines) > 1 or (len(lines) == 1 and len(lines[0]) > 15)
    
    if not is_substantial:
        return {**state, "is_valid": False, "fallback_message": "Please paste your code so I can help debug", "violation_type": "no_input"}
    
    # Use VERY lenient LLM - code is already substantial
    prompt = """
Determine if this is a VALID debug/analysis request.

Code is substantial. User is asking about it.

VALID QUERIES (Accept all of these):
- Error messages: "Stack overflow", "IndexError", "TLE", "Memory error", "Runtime error"
- Analysis: "Why does this fail?", "What's wrong?", "Why wrong answer?"
- Performance: "Too slow", "Memory limit exceeded"
- ANY question about their code: "How does this fail?", "Why does this not work?"

VALID because code is present.

INVALID only if:
- "just solve it" or "give me answer" → violation_type = solution_begging
- Completely off-topic and unrelated to code ("what is life?") → violation_type = off_topic

ASSUME GOOD FAITH: User provided code to debug.

Output:
- is_valid: true or false
- fallback_message: (empty if valid; explain why if invalid)
- violation_type: "ok", "solution_begging", or "off_topic"
"""

    input_text = f"Query: {state['user_query']}"
    res = run_guard_llm(prompt, input_text)
    return {**state, **res}

def guard_explain_code(state: GraphState) -> GraphState:
    # FIRST: Check if code is present AND non-trivial
    code = state['user_code'].strip()
    query = state['user_query'].strip()
    
    if not code or len(code) == 0:
        return {**state, "is_valid": False, "fallback_message": "Please paste the code you'd like me to explain", "violation_type": "no_input"}
    
    # Reject single-character or trivial code (single variable)
    if len(code) <= 2 or code in ['x', 'y', 'n', 'i', 'j', 'a', 'b']:
        return {**state, "is_valid": False, "fallback_message": "Please paste the code you'd like me to explain", "violation_type": "no_input"}
    
    # If query is present, validate it's actually asking for explanation (not clarification/off-topic)
    if query:
        prompt = """
You are a validator for "Explain Code" requests.

User pasted code and is asking a question about it.

VALID (is_valid=true) if user is asking:
- Explanation of how code works
- What specific lines/functions do
- How this approach solves the DSA problem
- Why specific logic is used
- Time/space complexity
- How to optimize code

INVALID (is_valid=false) if user is:
- Asking clarification about problem (ask in Clarify button)
- Asking about problem constraints/format (ask in Clarify button)
- Asking definitions or theory (ask in Clarify button)
- Asking off-topic question unrelated to their code
- Asking to debug/fix the code (ask in Debug button)

Be strict: If it's clarification or off-topic, reject it.

Output:
- is_valid: true or false
- fallback_message: "For problem clarification, use the Clarify button" (if clarification) or "Please ask about your code" (if off-topic)
- violation_type: "wrong_button" (if clarification) or "off_topic" (if unrelated)
"""
        res = run_guard_llm(prompt, f"Code: {code}\nQuery: {query}")
        return {**state, **res}
    
    # No query provided - code alone is sufficient for explanation
    return {**state, "is_valid": True, "fallback_message": "", "violation_type": "ok"}

def guard_validate_approach(state: GraphState) -> GraphState:
    query = state['user_query'].strip()
    code = state['user_code'].strip()
    
    # FIRST: Check for empty input - accept if either query OR code is present
    if not query and not code:
        return {**state, "is_valid": False, "fallback_message": "Please share your approach idea or code", "violation_type": "no_input"}
    
    # If code is present without query, accept it - can infer approach from code
    if code and not query:
        return {**state, "is_valid": True, "fallback_message": "", "violation_type": "ok"}
    
    prompt = """
You are a lenient validator for approach validation requests.

User clicked "Validate" button to check if their idea makes sense for the problem.

ACCEPT (is_valid=true) if user is:
- Proposing an approach ("Can I use...?", "Should I...?")
- Classifying the problem type ("Is this a Graph problem?", "Is this DP?")
- Asking about feasibility of an idea
- Asking about complexity/efficiency
- Any question that shows they're thinking about the problem

ONLY REJECT (is_valid=false) if user:
- Explicitly asks for solution code
- Asks for hints (that's the Hint button)
- Provides no input at all (no_input)
- Completely off-topic

Default: ACCEPT. User clicked Validate button, so accept their approach questions.

If INVALID:
- is_valid = false
- violation_type = "no_input" (if empty), "wrong_button" (if asking for hints), or "solution_begging" (if asking for code)

If VALID:
- is_valid = true
- fallback_message = ""
- violation_type = "ok"
"""


    res = run_guard_llm(prompt, f"Query: {state['user_query']}")
    return {**state, **res}

def guard_clarification(state: GraphState) -> GraphState:
    # Check for empty input
    if not state['user_query'] or not state['user_query'].strip():
        return {**state, "is_valid": False, "fallback_message": "Please ask a question about the problem statement.", "violation_type": "no_input"}
    
    # Use lenient LLM - accept most clarification-related questions
    prompt = """
You are a lenient validator for problem clarification requests.

User clicked the "Clarify" button to understand the problem better.

ACCEPT (is_valid=true) if user is asking about:
- Problem details, constraints, data properties
- Input/output format
- What terms mean
- Examples or test cases
- Any aspect of understanding the problem statement

ONLY REJECT (is_valid=false) if user explicitly asks for:
- How to solve (that's the Hint button)
- Algorithm or approach advice (that's Validate button)
- Complete solution (that's never allowed)
- Completely off-topic nonsense unrelated to the problem

Default: ACCEPT. User clicked Clarify for a reason.

If INVALID:
- violation_type = "wrong_button" (if asking how to solve)
- fallback_message = "For solution guidance, use the Hint button. Here, I can clarify problem details."

If VALID:
- is_valid = true
- fallback_message = ""
- violation_type = "ok"
"""

    res = run_guard_llm(prompt, f"Query: {state['user_query']}")
    return {**state, **res}

# ===============================
# 6. HANDLERS & FALLBACK
# ===============================
def handle_how_to_solve_this(state: GraphState): return {**state, "answer": "LLM: Generating Hint..."}
def handle_why_my_code_failed(state: GraphState): return {**state, "answer": "LLM: Analyzing Bug..."}
def handle_explain_my_code(state: GraphState): return {**state, "answer": "LLM: Explaining Code..."}
def handle_validate_my_approach(state: GraphState): return {**state, "answer": "LLM: Validating Idea..."}
def handle_clarification_request(state: GraphState): return {**state, "answer": "LLM: Clarifying Constraints..."}

def handle_fallback(state: GraphState) -> GraphState:
    return {**state, "answer": state["fallback_message"]}

# ===============================
# 7. GRAPH BUILD
# ===============================
build = StateGraph(GraphState, input_schema=InputState, output_schema=OutputState)

build.add_node("setup", setup_node)

# Guards
build.add_node("guard_how_to_solve", guard_how_to_solve)
build.add_node("guard_why_failed", guard_why_failed)
build.add_node("guard_explain_code", guard_explain_code)
build.add_node("guard_validate", guard_validate_approach)
build.add_node("guard_clarification", guard_clarification)

# Handlers
build.add_node("handle_how_to_solve", handle_how_to_solve_this)
build.add_node("handle_why_failed", handle_why_my_code_failed)
build.add_node("handle_explain", handle_explain_my_code)
build.add_node("handle_validate", handle_validate_my_approach)
build.add_node("handle_clarification", handle_clarification_request)
build.add_node("handle_fallback", handle_fallback)

build.add_edge(START, "setup")

INTENT_TO_GUARD = {
    "how_to_solve_this": "guard_how_to_solve",
    "why_my_code_failed": "guard_why_failed",
    "explain_my_code": "guard_explain_code",
    "validate_my_approach": "guard_validate",
    "clarification_request": "guard_clarification",
}
INTENT_TO_GUARD = {
    "how_to_solve_this": "guard_how_to_solve",
    "why_my_code_failed": "guard_why_failed",
    "explain_my_code": "guard_explain_code",
    "validate_my_approach": "guard_validate",
    "clarification_request": "guard_clarification",
}
def route_to_guard(state: GraphState):
    return state["user_intent"]
build.add_conditional_edges("setup", route_to_guard,INTENT_TO_GUARD)

def check_validity(state: GraphState):
    return "proceed" if state["is_valid"] else "fallback"

guards_to_handlers = {
    "guard_how_to_solve": "handle_how_to_solve",
    "guard_why_failed": "handle_why_failed",
    "guard_explain_code": "handle_explain",
    "guard_validate": "handle_validate",
    "guard_clarification": "handle_clarification"
}

for guard, handler in guards_to_handlers.items():
    build.add_conditional_edges(
        guard,
        check_validity,
        {"proceed": handler, "fallback": "handle_fallback"}
    )
    build.add_edge(handler, END)

build.add_edge("handle_fallback", END)
graph = build.compile()
