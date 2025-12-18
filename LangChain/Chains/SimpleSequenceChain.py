from Models.groq import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Prompt 1 → Generate baby name
name_prompt = PromptTemplate.from_template(
    "Suggest a Single baby name from the country {country} for a {gender}."
)

# Prompt 2 → Generate jobs for that name
job_prompt = PromptTemplate.from_template(
    "Suggest Single job based on this name: {name} and reason why it will fit based on astrology."
)

output_parser=StrOutputParser()
chain=name_prompt|llm|output_parser|job_prompt|llm|output_parser
country = input("Country: ").strip().lower()
gender_input = int(input("Gender (1=Male, 2=Female): ").strip())
gender = "Male" if gender_input == 1 else "Female"
resp = chain.invoke({"country": country, "gender": gender})
print(resp)
