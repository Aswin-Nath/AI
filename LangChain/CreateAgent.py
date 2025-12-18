# from Models.flash import llm
# from Models.local_llm import llm
# from Mode.groq import llm
from Models.groq import llm
from langchain.agents import create_agent
from langchain.tools import tool
@tool
def find_value(city:str):
    """
    Find the actual ascii values of the characters of the city and sum it and return the value
    
    :param city: Description
    :type city: str
    """
    return sum(ord(i) for i in city)
system_prompt="""
you are a full time mathematician who is good at solving complex calculations and math problems
"""

@tool
def find_numeric_value(a:int,b:int):
    """
    This is return the multiplication of the two numbers
    
    :param a: Description
    :type a: int
    :param b: Description
    :type b: int
    """
    print("tool invoked")
    return a*b
agent=create_agent(llm,tools=[find_value,find_numeric_value],system_prompt=system_prompt)

question = "print the value of 5 and 5"
for step in agent.stream({"messages": question},stream_mode="values"):
    step["messages"][-1].pretty_print()
