from pydantic import BaseModel
from typing import List
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import create_agent
from Models.groq import llm
from tools_client.Tavily import tavily_tool
wiki_tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=2,doc_content_chars_max=2000))


SYSTEM_PROMPT="""
Rules:
- First use Wikipedia or Tavily to verify current Chief Ministers.
- Then populate the structured output.
- Do NOT fill fields without tool verification.
"""

class Output(BaseModel):
    """
    return two list one is state_name and another one is cm_name make sure they match in count
    """
    states:List[str]
    cms:List[str]



research_agent = create_agent(
    llm,
    tools=[wiki_tool, tavily_tool],
    system_prompt="""
    you are helpful assistant
    Rules
    - Use Tavily_tool for searching in the web
    - Use the Wikipedia to get the wikipedia content
    - Provide the output in the structured format as Output Mode
    - Verify CM names from at least ONE Wikipedia page.
    - Cross-check with a recent news source if available.
    - Prefer the most recently updated source.
    """
    ,response_format=Output
)

research_result = research_agent.invoke(
    {"messages": "List current chief ministers of Indian states"}
)

raw_text = research_result["structured_response"]

print(raw_text)