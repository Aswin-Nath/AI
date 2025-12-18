from langchain_community.retrievers import WikipediaRetriever
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import create_agent
from Models.groq import llm
wiki_tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=2,doc_content_chars_max=2000))


SYSTEM_PROMPT="""
Rules:
- Call the Wikipedia tool exactly once.
- Use only the first relevant page.
- Do not make follow-up Wikipedia calls.
- Produce the final answer immediately after the tool result.
"""
agent=create_agent(llm,tools=[wiki_tool],system_prompt=SYSTEM_PROMPT)

for token in agent.stream({"messages":"List out the states of the India"},stream_mode="values"):
    print(token["messages"][-1].pretty_print())