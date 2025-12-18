from Models.groq import llm
from langchain.agents import create_agent
from langchain.tools import tool
from tools_client.Tavily import tavily_tool

@tool(
    "Sum_of_digits",
    description="This tool will return the sum of digits of a number"
)
def sum_of_digits(x:int):
    """
    Docstring for sum_of_digits
    
    :param x: Description
    :type x: int
    """
    summation=0
    for i in str(x):
        summation+=int(i)
    
    return summation
@tool(
    "multiply_two_numbers",
    description="""
    get two numbers as input and return the result of their multiplication
"""
)
def multiply_number(x:int,y:int):
    """
    Docstring for multiple_number
    
    :param x: Description
    :type x: int
    :param y: Description
    :type y: int
    """
    return x*y

agent=create_agent(llm,tools=[tavily_tool,sum_of_digits,multiply_number])

for token in agent.stream({"messages":"return the sum of digits of the year where italy won the first football world cup and multiply with the sum of digits of the year germany won their last football world cup"},stream_mode="values"):
    print(token["messages"][-1].pretty_print())