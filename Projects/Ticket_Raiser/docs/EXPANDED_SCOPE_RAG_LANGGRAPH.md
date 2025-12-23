# 🚀 **EXPANDED SCOPE - RAG + LangGraph Architecture**

## **VISION**
Transform the DSA platform from a simple problem-solving hub into an **AI-powered intelligent teaching & learning system** with real-time issue detection and automated resolution.

---

## **PART 1: RAG (RETRIEVAL AUGMENTED GENERATION) CAPABILITIES**

### **1.1 Knowledge Base Components**

#### **Educational Knowledge Base**
```
├── DSA Concepts (Recursion, DP, Graphs, etc.)
├── Common Patterns & Approaches
├── Code Examples & Solutions
├── Algorithm Complexity Analysis
├── Common Pitfalls & Mistakes
├── Interview Preparation Resources
└── Community Solutions & Discussions
```

**Implementation:**
- Vector embeddings for DSA concepts (OpenAI embeddings)
- Pinecone/Weaviate vector store for similarity search
- Chunk optimization: Problem context + relevant concepts
- Semantic search: "How to solve DP problems?" → Retrieve patterns

#### **Problem-Specific Knowledge**
```
├── Problem Statement & Variations
├── Test Case Explanations
├── Editorial Solutions
├── Common Wrong Approaches
├── Optimal vs Brute Force Trade-offs
├── Time/Space Complexity Notes
└── Real-world Applications
```

#### **User Progress Knowledge**
```
├── User's Solved Problems
├── Common Mistakes Pattern
├── Learning Path Progress
├── Difficulty Level Progression
├── Topic Mastery Assessment
└── Personalized Weakness Areas
```

---

### **1.2 RAG-Powered Features**

#### **A. Intelligent Chat Assistant (In Code Editor)**
```
Current: Simple chat UI exists
Enhanced:

1. CONTEXT-AWARE HELP
   User asks: "How do I approach this?"
   System:
   - Retrieve problem statement
   - Get similar solved problems from user's history
   - Fetch DSA concept explanations
   - Provide personalized hint (not full solution)
   
2. CODE EXPLANATION
   User asks: "Explain my code"
   System:
   - Analyze user's code
   - Retrieve similar patterns from knowledge base
   - Explain complexity with retrieved examples
   
3. DEBUGGING ASSISTANT
   User says: "Why am I getting WRONG_ANSWER?"
   System:
   - Retrieve problem test cases
   - Analyze code for common pitfalls
   - Suggest debugging approach with examples
   - No direct solution, just guidance

4. CONCEPT TEACHING
   User asks: "What is DP?"
   System:
   - Retrieve DP concept explanation
   - Get problems user can solve first (easy ones)
   - Provide step-by-step approach
   - Link to related problems

5. OPTIMIZATION HINTS
   User says: "My solution is too slow"
   System:
   - Retrieve faster algorithms for this problem
   - Show complexity comparisons
   - Suggest optimization patterns
   - Point to similar optimized solutions
```

**Example Implementation:**
```python
class ChatAssistant:
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store  # Pinecone
        self.llm = llm  # Claude
        
    async def get_hint(self, problem_id, user_code, question):
        # Get context
        problem = get_problem(problem_id)
        similar_problems = await self.vector_store.search(
            query=problem.description,
            filter={"user_id": user_id, "solved": True},
            top_k=3
        )
        dsa_concepts = await self.vector_store.search(
            query=question,
            filter={"type": "concept"},
            top_k=2
        )
        
        # Build prompt with retrieved context
        prompt = f"""
        Problem: {problem.title}
        User's Code: {user_code}
        User Question: {question}
        
        Similar solved problems user did:
        {similar_problems}
        
        Relevant DSA concepts:
        {dsa_concepts}
        
        Provide a HINT (not solution), guiding them with concepts they know
        """
        
        return await self.llm.generate(prompt)
```

---

#### **B. Personalized Learning Paths**
```
RAG-Powered Path Generation:

1. ASSESS USER LEVEL
   Input: User's solved problems
   RAG:
   - Retrieve topic difficulty data
   - Analyze user's weak areas
   - Get recommended prerequisite problems
   Output: "You're strong in Arrays, weak in Graphs"

2. CREATE CUSTOM PATH
   RAG:
   - Retrieve problems ordered by difficulty
   - Find concept-prerequisite mappings
   - Get optimal problem order
   - Suggest daily goals based on performance
   
3. ADAPTIVE RECOMMENDATIONS
   Today's Problem: DP problem failed
   RAG:
   - Retrieve easier DP problems user hasn't solved
   - Get DP concept explanations
   - Suggest 2-3 simpler problems to understand concept first
   - Then retry original problem

Example Path:
Day 1: Easy Array → Easy Prefix Sum
Day 2: Medium DP (Coin Change) → Medium DP
Day 3: Hard DP (0/1 Knapsack) → Interview Problem
```

---

#### **C. Solution Comparison & Learning**
```
When user submits code:

1. ACCEPTED SOLUTION
   Retrieve:
   - Optimal solution from editorial
   - User's previous solutions for same problem
   - Similar problems' solutions
   
   Compare:
   - Time/Space complexity
   - Code patterns & idioms
   - Edge case handling
   
   Learning Output:
   - "You used approach A (O(n²)), optimal is B (O(n log n))"
   - "Here's a cleaner way to write this pattern"
   - "This problem teaches concept X used in these 5 other problems"

2. WRONG ANSWER
   Retrieve:
   - Test cases with explanations
   - Common mistakes for this problem
   - Similar problems where user succeeded
   
   Debug Output:
   - "You're not handling edge case: empty array"
   - "This is a graph problem, you're treating as array"
   - "Try this simpler problem first: problem_id"
```

---

### **1.3 RAG Data Architecture**

```
Vector Store Chunking Strategy:

CHUNK 1: Problem Context
- Problem Title + ID
- Full Description
- Constraints
- Examples
→ Vector size: 512 tokens

CHUNK 2: Concept Explanation
- Concept Name
- Definition
- Complexity Analysis
- When to use
→ Vector size: 1024 tokens

CHUNK 3: Solution Pattern
- Algorithm approach
- Code snippet
- Complexity
- When applicable
→ Vector size: 1024 tokens

CHUNK 4: Common Mistakes
- What users often do wrong
- Why it's wrong
- How to fix it
→ Vector size: 512 tokens

CHUNK 5: Test Case Explanation
- Input/Output walkthrough
- Edge cases covered
→ Vector size: 512 tokens

Metadata for filtering:
{
  "problem_id": 123,
  "topic": "dynamic_programming",
  "difficulty": "medium",
  "solved_by_user": true,
  "chunk_type": "concept",
  "language": "python",
  "rating": 4.5
}
```

---

## **PART 2: LangGraph WORKFLOW ARCHITECTURES**

### **2.1 Teaching Workflow Graph**

```
┌─────────────────────────────────────────────────────────┐
│         USER STARTS SOLVING PROBLEM                      │
└────────────────────┬────────────────────────────────────┘
                     │
           ┌─────────▼──────────┐
           │  Assess User Level │
           │  (Problems solved) │
           └─────────┬──────────┘
                     │
        ┌────────────▼──────────────┐
        │ Route to Teaching Path    │
        │ (Beginner/Intermediate/   │
        │  Advanced)                │
        └────────────┬──────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
Beginner Path   Intermediate Path   Advanced Path
 (Concepts)      (Patterns)         (Optimization)
    │                │                │
    └────────────────┼────────────────┘
                     │
           ┌─────────▼──────────┐
           │  Monitor Progress  │
           └─────────┬──────────┘
                     │
        ┌────────────▼──────────────┐
        │ Problem Solved?           │
        └────┬──────────────────┬───┘
             │ YES              │ NO
             │                  │
             ▼                  ▼
         ┌────────┐      ┌─────────────┐
         │Celebrate       │Smart Hints  │
         │+ Unlock Next   │+ Simpler    │
         └────────┘       │  Problems   │
                          └─────────────┘
```

**LangGraph Implementation:**
```python
from langgraph.graph import StateGraph
from typing import Literal

class TeachingState(TypedDict):
    user_id: str
    problem_id: int
    user_code: str
    attempts: int
    solved: bool
    difficulty_level: Literal["beginner", "intermediate", "advanced"]
    hints_given: List[str]
    next_action: Literal["teach_concept", "give_hint", "suggest_simpler"]

graph = StateGraph(TeachingState)

graph.add_node("assess_level", assess_user_level)
graph.add_node("route_teaching", route_teaching_path)
graph.add_node("teach_concept", teach_dsa_concept)
graph.add_node("give_hint", give_contextual_hint)
graph.add_node("check_solution", check_solution)
graph.add_node("suggest_simpler", suggest_prerequisite_problem)
graph.add_node("celebrate", celebrate_success)

graph.add_edge("START", "assess_level")
graph.add_edge("assess_level", "route_teaching")
graph.add_conditional_edges(
    "route_teaching",
    lambda x: x["difficulty_level"],
    {
        "beginner": "teach_concept",
        "intermediate": "give_hint",
        "advanced": "check_solution"
    }
)
graph.add_edge("teach_concept", "check_solution")
graph.add_edge("give_hint", "check_solution")
graph.add_conditional_edges(
    "check_solution",
    lambda x: "celebrate" if x["solved"] else "suggest_simpler"
)
```

---

### **2.2 Issue Detection & Reporting Workflow**

```
┌──────────────────────────────────────────────────────┐
│    USER REPORTS ISSUE                                 │
│    (Wrong test case / Bad editorial / Wrong answer)  │
└────────────────────┬─────────────────────────────────┘
                     │
           ┌─────────▼──────────────┐
           │ Classify Issue Type    │
           │ (LLM Classification)   │
           └─────────┬──────────────┘
                     │
    ┌────────────────┼──────────────────┐
    │                │                  │
    ▼                ▼                  ▼
TEST_CASE      PROBLEM_INFO         EDITORIAL
    │                │                  │
    ├─────┬──────────┼────────┬─────────┤
    │     │          │        │         │
    ▼     ▼          ▼        ▼         ▼
  Verify Code       Get       Verify    Editorial
  Against Test      Problem   Answer    Correctness
  Case Output       Description         Check
    │                │                  │
    ├─────────────────┼──────────────────┤
    │                                    │
    ┌────────────────▼────────────────┐
    │ Is Issue Valid?                  │
    └────┬──────────────────────────┬──┘
         │ YES                      │ NO
         │                          │
         ▼                          ▼
    ┌─────────┐            ┌────────────────┐
    │ Raise   │            │ Notify User:   │
    │ Ticket  │            │ "Not a valid   │
    │ + Email │            │  issue"        │
    └─────────┘            └────────────────┘
         │
         ▼
    ┌─────────────────┐
    │ Admin Dashboard │
    │ (Fix Issue)     │
    └─────────────────┘
```

**LangGraph Implementation:**
```python
class IssueDetectionState(TypedDict):
    issue_description: str
    problem_id: int
    submission_id: Optional[int]
    user_id: str
    issue_type: Literal["TEST_CASE", "PROBLEM_INFO", "EDITORIAL"]
    is_valid: bool
    confidence: float
    reasoning: str
    ticket_id: Optional[str]

async def classify_issue(state: IssueDetectionState) -> IssueDetectionState:
    """Use LLM to classify issue type with RAG context"""
    problem = get_problem(state["problem_id"])
    similar_issues = await vector_store.search(
        query=state["issue_description"],
        filter={"type": "reported_issue"},
        top_k=3
    )
    
    prompt = f"""
    Problem: {problem.title}
    User's Issue: {state['issue_description']}
    
    Similar reported issues: {similar_issues}
    
    Classify this into: TEST_CASE (wrong test case), 
    PROBLEM_INFO (wrong description/constraints),
    EDITORIAL (wrong solution)
    
    Provide: type, confidence (0-1), reasoning
    """
    
    classification = await llm.generate(prompt)
    return {
        **state,
        "issue_type": classification["type"],
        "confidence": classification["confidence"],
        "reasoning": classification["reasoning"]
    }

async def verify_test_case(state: IssueDetectionState) -> IssueDetectionState:
    """Check if test case is actually wrong"""
    problem = get_problem(state["problem_id"])
    submission = get_submission(state["submission_id"])
    test_cases = get_test_cases(problem.id)
    
    # Run solution against all test cases
    results = []
    for tc in test_cases:
        result = await run_code(submission.code, tc.input_data)
        results.append({
            "expected": tc.expected_output,
            "actual": result,
            "match": result == tc.expected_output
        })
    
    issue_is_valid = any(not r["match"] for r in results)
    
    return {
        **state,
        "is_valid": issue_is_valid,
        "test_results": results
    }

async def verify_problem_info(state: IssueDetectionState) -> IssueDetectionState:
    """Check if problem info is correct"""
    problem = get_problem(state["problem_id"])
    
    # Use LLM to compare reported issue with actual problem
    prompt = f"""
    Problem: {problem.title}
    Description: {problem.description}
    Constraints: {problem.constraints}
    
    User's Issue: {state['issue_description']}
    
    Is the user correct that there's an issue with 
    problem description or constraints?
    
    Provide: valid (bool), reasoning
    """
    
    verification = await llm.generate(prompt)
    
    return {
        **state,
        "is_valid": verification["valid"],
        "reasoning": verification["reasoning"]
    }

async def verify_editorial(state: IssueDetectionState) -> IssueDetectionState:
    """Check if editorial solution is correct"""
    problem = get_problem(state["problem_id"])
    editorial = get_editorial(problem.id)
    test_cases = get_test_cases(problem.id)
    
    if not editorial:
        return {**state, "is_valid": True}  # No editorial to verify
    
    # Run editorial code against all test cases
    results = []
    for tc in test_cases:
        try:
            result = await run_code(editorial.code, tc.input_data)
            results.append({
                "test_case_id": tc.id,
                "passed": result == tc.expected_output
            })
        except Exception as e:
            results.append({
                "test_case_id": tc.id,
                "passed": False,
                "error": str(e)
            })
    
    is_valid = all(r["passed"] for r in results)
    
    return {
        **state,
        "is_valid": not is_valid,  # Valid issue if editorial FAILS
        "test_results": results
    }

# Build graph
graph = StateGraph(IssueDetectionState)
graph.add_node("classify", classify_issue)
graph.add_node("verify_test_case", verify_test_case)
graph.add_node("verify_problem_info", verify_problem_info)
graph.add_node("verify_editorial", verify_editorial)
graph.add_node("raise_ticket", raise_ticket)
graph.add_node("notify_user", notify_user)

graph.add_edge("START", "classify")
graph.add_conditional_edges(
    "classify",
    lambda x: x["issue_type"],
    {
        "TEST_CASE": "verify_test_case",
        "PROBLEM_INFO": "verify_problem_info",
        "EDITORIAL": "verify_editorial"
    }
)

graph.add_conditional_edges(
    "verify_test_case",
    lambda x: "raise_ticket" if x["is_valid"] else "notify_user"
)
# ... similar for other verifications
```

---

### **2.3 Smart Question Refinement Workflow**

```
┌──────────────────────────────────────────────────┐
│  ADMIN: Question Might Be Wrong                  │
│  Needs Verification Before Raising Ticket        │
└────────────────────┬─────────────────────────────┘
                     │
           ┌─────────▼──────────────┐
           │ Fetch Problem Details  │
           └─────────┬──────────────┘
                     │
           ┌─────────▼──────────────┐
           │ Get All Submissions    │
           │ For This Problem       │
           └─────────┬──────────────┘
                     │
           ┌─────────▼──────────────┐
           │ Analyze Patterns       │
           │ (Pass/Fail rates)      │
           └─────────┬──────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
High Pass Rate   Medium Rate       Low Pass Rate
(Question Good)  (Need Review)    (Likely Wrong)
    │                │                │
    ▼                ▼                ▼
 Archive        Flag for          Raise Issue
             Review by
             Problem Creator
```

---

## **PART 3: INTEGRATED TEACHING SYSTEM**

### **3.1 Complete User Journey**

```
USER FLOW WITH RAG + LangGraph:

1. USER STARTS PROBLEM
   ↓
   [RAG] Retrieve:
   - User's profile + weak areas
   - Similar problems they've solved
   - Prerequisites they know
   ↓
   
2. SHOWS SMART INTERFACE
   - "You've solved 3 similar problems"
   - "Prerequisite: Recursion (you know this!)"
   - Suggest "Easy" version first
   ↓
   
3. USER WRITES CODE + ASKS QUESTION
   (e.g., "How do I optimize this?")
   ↓
   [RAG] Retrieve:
   - Problem context
   - Similar optimization patterns
   - Relevant DSA concepts
   [LLM] Generate personalized hint
   ↓
   
4. USER GETS CONTEXTUAL HELP
   - "Like problem 45 you solved, try this approach"
   - "This needs DP. Check out this simpler DP problem first"
   - "Your current solution is O(n²), try memoization"
   ↓
   
5. USER SUBMITS CODE
   ↓
   Decision Tree:
   ├─ ACCEPTED → Show optimal solution comparison
   │            → Unlock next problem
   │            → Suggest related problems
   │
   ├─ WRONG_ANSWER → [RAG] Retrieve common mistakes
   │                → Debug hints with examples
   │                → Suggest simpler version
   │
   └─ ERROR → [RAG] Get debugging tips
            → Suggest concept review
            → Show working solution pattern

6. USER REPORTS ISSUE
   ↓
   [LangGraph] Auto-verify claim:
   - Is test case really wrong?
   - Is description unclear?
   - Is editorial solution wrong?
   ↓
   If Valid: Raise ticket + Notify user
   If Invalid: Educate user why it's valid
```

---

### **3.2 Teaching Features by Problem Type**

#### **Easy Problems**
```
Focus: Concept Understanding
- Provide full hints with code templates
- Explain every step
- Connect to prerequisites
- Celebrate small wins
- Move user to next natural problem
```

#### **Medium Problems**
```
Focus: Pattern Recognition
- Suggest approach without code
- Compare multiple strategies
- Show complexity trade-offs
- Guide optimization path
- Relate to real-world scenarios
```

#### **Hard Problems**
```
Focus: Problem-Solving Skills
- Ask leading questions only
- No direct hints
- Suggest similar medium problems
- Discuss time/space optimization
- Prepare for interviews
```

---

## **PART 4: IMPLEMENTATION ROADMAP**

### **Phase 1: Foundation (Weeks 1-2)**
```
✓ Set up vector store (Pinecone)
✓ Create problem embedding pipeline
✓ Build RAG retrieval service
✓ Set up LangGraph framework
□ Implement basic chat with RAG
□ Create concept knowledge base
```

### **Phase 2: Teaching System (Weeks 3-4)**
```
□ Implement hint generation
□ Build learning path algorithm
□ Create concept recommendations
□ Add solution comparison feature
□ Connect chat to problem context
```

### **Phase 3: Issue Detection (Weeks 5-6)**
```
□ Build issue classification workflow
□ Implement test case verification
□ Create problem info validator
□ Add editorial verification
□ Set up admin dashboard
□ Add email notifications
```

### **Phase 4: Advanced Features (Weeks 7-8)**
```
□ Personalized learning paths
□ Adaptive difficulty adjustment
□ Community solutions discussion
□ Interview preparation mode
□ Analytics & insights
```

---

## **PART 5: API ADDITIONS NEEDED**

### **Chat & Teaching APIs**
```
POST   /chat/message
- problem_id: int
- message: str
- submission_id?: int
Response: { message, hints, related_problems, concepts }

GET    /problems/{id}/similar
- Filter by difficulty, topic, solved status
Response: [ { id, title, difficulty, why_similar } ]

GET    /learning/path
- user_id: str
Response: { current_level, recommended_next, weak_areas }

POST   /concepts/explain
- concept: str
- context?: problem_id
Response: { explanation, examples, related_problems }

GET    /submissions/{id}/feedback
- Intelligent analysis of code
Response: { approach, complexity, improvements, pattern_name }
```

### **Issue Detection APIs**
```
POST   /issues/verify
- issue_description: str
- problem_id: int
- submission_id?: int
Response: { is_valid, confidence, issue_type, reasoning }

GET    /admin/issues
- status?: str (open, closed, reviewing)
Response: [ { id, type, problem_id, status, validation } ]

PUT    /admin/issues/{id}/resolve
- resolution: str
- action: "fix_test_case" | "update_description" | etc
Response: { ticket_id, changes_made }
```

---

## **PART 6: TECHNOLOGY STACK**

```
LLM & NLP:
- Claude 3.5 Sonnet (for teaching & verification)
- OpenAI Embeddings (for semantic search)
- LangGraph (for workflow orchestration)

Vector Store:
- Pinecone (managed vector database)
- Alternative: Weaviate, Milvus

Backend Additions:
- LangChain (for RAG pipeline)
- Redis (for caching embeddings)
- Bull Queue (for async verification jobs)

Frontend Enhancements:
- React Query (for real-time chat)
- Markdown renderer (for concept explanations)
- Code diff viewer (for solution comparison)
```

---

## **PART 7: EXAMPLE USER STORIES**

### **Story 1: Guided Learning**
```
Given: User attempted DP problem, got WRONG_ANSWER
When: User clicks "Need Help?"
Then: System should:
  1. Identify user hasn't solved DP problems
  2. Retrieve 2 easier DP problems user can solve
  3. Suggest: "Solve these DP problems first to understand concept"
  4. Provide dynamic programming explanation with examples
  5. After solving those, guide back to original problem
```

### **Story 2: Smart Issue Detection**
```
Given: User reports "Test case output is wrong"
When: User provides evidence
Then: System should:
  1. Classify issue as TEST_CASE_REPORT
  2. Run user's code against all test cases
  3. Verify if test case output truly doesn't match
  4. If valid: Raise ticket, notify user "Thank you, we're fixing it"
  5. If invalid: Educate user why their code is wrong, not test case
```

### **Story 3: Contextual Teaching**
```
Given: User in code editor for problem 45
When: User asks "How do I optimize?"
Then: System should:
  1. Retrieve problem context
  2. Find similar problems user solved (30, 40)
  3. Get optimization patterns (memoization, space optimization)
  4. Generate: "Like in problem 30, try memoization here.
               Current: O(2^n), With memo: O(n)"
  5. Link to article on memoization
```

---

## **PART 8: COMPETITIVE ADVANTAGES**

```
vs LeetCode:
✓ Context-aware teaching (knows user's history)
✓ Prevents cheating (detects copy-paste)
✓ Guides to solution vs just showing it
✓ Personalized learning paths
✓ Smart issue detection (not user-reported spam)

vs CodeSignal:
✓ Open-ended problems with guidance
✓ Community learning + AI teaching
✓ Automatic quality assurance via LLM
✓ Real-time hint generation

vs Internal Training:
✓ Scales without hiring instructors
✓ 24/7 availability
✓ Personalized to each learner
✓ Data-driven insights
```

---

## **SUMMARY MATRIX**

| Feature | RAG Required | LangGraph Required | Priority |
|---------|-------------|------------------|----------|
| Smart Chat Hints | ✅ | ✅ | P0 |
| Concept Explanations | ✅ | ❌ | P0 |
| Issue Detection | ✅ | ✅ | P1 |
| Learning Paths | ✅ | ✅ | P1 |
| Solution Comparison | ✅ | ❌ | P1 |
| Problem Validation | ❌ | ✅ | P2 |
| Interview Mode | ✅ | ❌ | P2 |
| Analytics | ❌ | ❌ | P3 |

---

## **NEXT STEPS**

1. **Finalize scope** - Which features to prioritize?
2. **Procurement** - Set up Pinecone account, API keys
3. **Data pipeline** - Embed existing problems & concepts
4. **Architecture design** - Detailed LangGraph graphs
5. **Backend skeleton** - API routes for RAG + LangGraph
6. **Frontend integration** - Chat UI enhancements

**Estimated Timeline:** 8 weeks for full implementation

---

**Generated:** December 23, 2025  
**Status:** 🚀 Ready for Implementation
