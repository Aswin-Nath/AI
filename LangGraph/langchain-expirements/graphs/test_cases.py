# # List of test cases with expected intents for verification
# test_cases = [
#     # --- HARDENING TESTS (Out of Scope) ---
#     {
#         "input": {"user_query": "When did the Taliban start ruling Afghanistan?", "user_code": None},
#         "expected": "i_cant_answer_to_this",
#         "desc": "Political history query"
#     },
#     {
#         "input": {"user_query": "What is the weather in Tokyo right now?", "user_code": None},
#         "expected": "i_cant_answer_to_this",
#         "desc": "General conversational query"
#     },
#     {
#         "input": {"user_query": "Who won the 2024 US Elections?", "user_code": None},
#         "expected": "i_cant_answer_to_this",
#         "desc": "Recent events/Politics"
#     },
#     {
#         "input": {"user_query": "Write me a love poem.", "user_code": None},
#         "expected": "i_cant_answer_to_this",
#         "desc": "Creative writing request"
#     },
#     {
#         "input": {"user_query": "Who invented the Python programming language?", "user_code": None},
#         "expected": "i_cant_answer_to_this",
#         "desc": "Computer History (often tricky, but strictly not CP help)"
#     },

#     # --- CLARIFICATION REQUESTS ---
#     {
#         "input": {"user_query": "What is the maximum value of N in this problem?", "user_code": None},
#         "expected": "clarification_request",
#         "desc": "Constraint query"
#     },
#     {
#         "input": {"user_query": "Does the input array contain negative numbers?", "user_code": None},
#         "expected": "clarification_request",
#         "desc": "Input format clarification"
#     },
#     {
#         "input": {"user_query": "What does 'lexicographically smallest' mean in this context?", "user_code": None},
#         "expected": "clarification_request",
#         "desc": "Problem statement terminology"
#     },

#     # --- PROBLEM SOLVING & STRATEGY ---
#     {
#         "input": {"user_query": "I am stuck. How should I approach the 'Trapping Rain Water' problem?", "user_code": None},
#         "expected": "how_to_solve_this",
#         "desc": "Request for approach/hints"
#     },
#     {
#         "input": {"user_query": "Can you give me a hint for LeetCode 42?", "user_code": None},
#         "expected": "how_to_solve_this",
#         "desc": "Direct hint request"
#     },

#     # --- CODE DEBUGGING (Failures) ---
#     {
#         "input": {
#             "user_query": "Why am I getting TLE on test case 5?", 
#             "user_code": "for i in range(n): for j in range(n): ..."
#         },
#         "expected": "why_my_code_failed",
#         "desc": "Time Limit Exceeded debugging"
#     },
#     {
#         "input": {
#             "user_query": "My logic seems correct but I get Wrong Answer.", 
#             "user_code": "def solve(): return 0"
#         },
#         "expected": "why_my_code_failed",
#         "desc": "Wrong Answer debugging"
#     },

#     # --- CODE EXPLANATION ---
#     {
#         "input": {
#             "user_query": "Can you explain what this recursive function is doing?", 
#             "user_code": "def dfs(u): visited[u]=True..."
#         },
#         "expected": "explain_my_code",
#         "desc": "Code logic explanation"
#     },
#     {
#         "input": {
#             "user_query": "What is the time complexity of this solution?", 
#             "user_code": "while l < r: mid = (l+r)//2 ..."
#         },
#         "expected": "explain_my_code",
#         "desc": "Complexity analysis request"
#     },

#     # --- APPROACH VALIDATION ---
#     {
#         "input": {"user_query": "Will a greedy approach work for the Knapsack problem?", "user_code": None},
#         "expected": "validate_my_approach",
#         "desc": "Verifying an algorithm choice"
#     },
#     {
#         "input": {"user_query": "I'm thinking of using Union-Find to detect cycles. Is that optimal?", "user_code": None},
#         "expected": "validate_my_approach",
#         "desc": "Optimality check of an idea"
#     },

#     # --- GENERAL DSA CONCEPTS ---
#     {
#         "input": {"user_query": "How does Dijkstra's algorithm work?", "user_code": None},
#         "expected": "general_dsa_concept",
#         "desc": "Concept explanation (no specific problem)"
#     },
#     {
#         "input": {"user_query": "What is the difference between Segment Tree and Fenwick Tree?", "user_code": None},
#         "expected": "general_dsa_concept",
#         "desc": "Comparison of data structures"
#     },
#     {
#         "input": {"user_query": "Explain Master Theorem for recurrences.", "user_code": None},
#         "expected": "general_dsa_concept",
#         "desc": "Mathematical DSA concept"
#     },
    
#     # --- TRICKY BOUNDARY CASE ---
#     {
#         "input": {"user_query": "Is Python slow for competitive programming?", "user_code": None},
#         "expected": "general_dsa_concept", # or validate_my_approach
#         "desc": "Language specific meta-question (Should be treated as Concept/Advice, not 'Can't Answer')"
#     },
# ]

# # --- RUNNER ---
# print(f"{'TEST DESCRIPTION':<40} | {'PREDICTED':<25} | {'EXPECTED':<25} | {'STATUS'}")
# print("-" * 105)

# for case in test_cases:
#     # Invoke the graph
#     result = graph.invoke(case["input"])
#     print(result)
#     # # Extract predicted intent
#     # predicted = result["answer"]
#     # expected = case["expected"]
    
#     # # formatting output
#     # status = "✅ PASS" if predicted == expected else "❌ FAIL"
#     # desc = case['desc'][:37] + "..." if len(case['desc']) > 37 else case['desc']
    
#     print("---"*25)
#     # print(f"{desc:<40} | {predicted:<25} | {expected:<25} | {status}")