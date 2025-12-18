import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_classic.chains.llm import LLMChain
from Models.local_llm import llm
parser = StrOutputParser()

# Prompt 1 → Generate baby name
name_prompt = PromptTemplate.from_template(
    "Suggest a Single baby name from the country {country} for a {gender}."
)

# Prompt 2 → Generate jobs for that name
job_prompt = PromptTemplate.from_template(
    "Suggest Single job based on this name: {name} and reason why it will fit based on astrology."
)

# Convert the first LLM output → dict {name: output}
extract_name = RunnableLambda(lambda x: {"name": x})

# Build the chain
chain = (
    name_prompt
    | llm
    | parser
    | extract_name
    | job_prompt
    | llm
    | parser
)

country = input("Country: ").strip().lower()
gender_input = int(input("Gender (1=Male, 2=Female): ").strip())
gender = "Male" if gender_input == 1 else "Female"

resp = chain.invoke({"country": country, "gender": gender})
print(resp)
