from langchain_tavily import TavilySearch


tavily_tool=TavilySearch(max_result=5,search_depth="basic")
