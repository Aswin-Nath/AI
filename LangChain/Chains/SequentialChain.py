# Without Runnables the variable wiring happens automatically between the first and second prompt

from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.llm import LLMChain
from langchain_classic.chains.sequential import SequentialChain
from Models.groq import llm
name_prompt=PromptTemplate(input_variables=["country","gender"],template="suggest a name for a baby from country {country} and gender {gender}")
name_chain=LLMChain(llm=llm,prompt=name_prompt,output_key="name")

job_prompt=PromptTemplate(input_variables=["name","country","gender"],template="suggest a job for this baby with name {name} and from country {country} and gender {gender} and also provide the reason")
job_chain=LLMChain(llm=llm,prompt=job_prompt,output_key="job_reason")


SeqChain=SequentialChain(chains=[name_chain,job_chain],input_variables=["country","gender"],output_variables=["name","job_reason"],verbose=True)

country="india"
gender="female"

result=SeqChain.invoke({"country":country,"gender":gender})

print("\nBaby Name:", result["name"])
print("Job Suggestion:", result["job_reason"])


# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser
# from langchain_core.runnables import RunnableMap
# from pydantic import BaseModel
# from Models.groq import llm
# name_prompt=PromptTemplate.from_template("suggest a name for a baby from country {country} and gender {gender}")
# job_prompt=PromptTemplate.from_template("suggest a job for this baby with name {name} and from country {country} and gender {gender} and also provide the reason")
# parser=StrOutputParser()
# country="india"
# gender="female"
# class Output(BaseModel):
#     name: str
#     job: str
#     reason: str
# # Chain that produces the name
# name_chain = name_prompt | llm | parser
# parser = PydanticOutputParser(pydantic_object=Output)

# # Merge inputs properly
# pipeline = (
#     RunnableMap({
#         "name": name_chain,
#         "country": lambda x: x["country"],
#         "gender": lambda x: x["gender"],
#     })
#     | job_prompt
#     | llm
#     | parser
# )



# result=pipeline.invoke({"country":country,"gender":gender})

# print("\nBaby Name:", result)
# print("Job Suggestion:", result["job_reason"])




# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import PydanticOutputParser
# from pydantic import BaseModel
# from Models.groq import llm
# class Output(BaseModel):
#     name: str
#     job: str
#     reason: str

# parser = PydanticOutputParser(pydantic_object=Output)

# job_prompt = PromptTemplate.from_template(
#     """
#  You MUST return ONLY valid JSON.
#     No explanations. No markdown. No code.

#     {format_instructions}
#     """
# )

# chain = (
#     job_prompt.partial(format_instructions=parser.get_format_instructions())
#     | llm
#     | parser
# )

# result = chain.invoke({"country": "india", "gender": "female"})
# print(result)
