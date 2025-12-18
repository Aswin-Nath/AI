from Models.groq import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from langchain_core.runnables import RunnableLambda,RunnableBranch
from typing import Literal
class validity_output(BaseModel):
    question:str
    type:Literal["valid","ambiguous","invalid"]
validity_parser=PydanticOutputParser(pydantic_object=validity_output)
validity_prompt = PromptTemplate(
    input_variables=["question"],
    partial_variables={
        "format_instructions":validity_parser.get_format_instructions()
    },
    template="""

You are an expert on general topics.

Given the question:
{question}

- valid: factual, time-independent, and semantically correct
- ambiguous: factual but time-dependent or missing context
- invalid: semantically impossible or uses incorrect roles

Return as per below instruction

{format_instructions}
"""
)
validity_chain = prompt=validity_prompt | llm | validity_parser




class rewrite_output(BaseModel):
    question:str
rewrite_parser=PydanticOutputParser(pydantic_object=rewrite_output)
rewrite_prompt=PromptTemplate(input_variables=["question"],template="""
Rewrite this quesiton {question} without any ambiguity and grammar mistakes 
and 
refer below thing for output format 
{format_instructions}            
""",
partial_variables={"format_instructions":rewrite_parser.get_format_instructions()}
)
rewrite_chain=rewrite_prompt|llm|rewrite_parser


class intent_output(BaseModel):
    question:str
    intent: Literal["question", "definition", "comparison", "opinion"]
intent_parser=PydanticOutputParser(pydantic_object=intent_output)
intent_prompt=PromptTemplate(input_variables=["question"],template="""
classify this {question} based on these categories question,definition,comparison,opinion
Choose the PRIMARY intent only.
Ignore secondary requests.
Return exactly one intent.
return according to below format
{format_instructions}
""",
partial_variables={"format_instructions":intent_parser.get_format_instructions()}
)
intent_chain=intent_prompt|llm|intent_parser




class answer_output(BaseModel):
    question:str
    answer:str
answer_parser=PydanticOutputParser(pydantic_object=answer_output)
answer_prompt=PromptTemplate(input_variables=["question","type"],template="""
Answer for this question {question} which is of this type {type} and return in the below format
{format_instructions}
""",
partial_variables={"format_instructions":answer_parser.get_format_instructions()})
answer_chain=answer_prompt|llm|answer_parser


class summary_output(BaseModel):
    question:str
    summary:str
summary_parser=PydanticOutputParser(pydantic_object=summary_output)
summary_prompt=PromptTemplate(input_variables=["question","answer"],template="""
You have to summarize the answer with combining both questions and followed by the answer below i attached the quesiton and answer and now summarize that
question: {question} 
answer:   {answer}
{format_instructions}
""",
partial_variables={"format_instructions":summary_parser.get_format_instructions()})
summary_chain=summary_prompt|llm|summary_parser



pipeline=(
    validity_chain
    | RunnableBranch(
        (
        lambda x:x.type=="valid",
        RunnableLambda(lambda x:{"question":x.question})
        |rewrite_chain
        |RunnableLambda(lambda x:{"question":x.question})
        |intent_chain
        |RunnableBranch(
        (
        lambda x:x.intent!="opinion",
        RunnableLambda(lambda x:{"question":x.question,"type":x.intent})
        |answer_chain
        |RunnableLambda(lambda x:{"question":x.question,"answer":x.answer})
        |summary_chain  
        ),
        (
            RunnableLambda(lambda _:"sorry i cant answer to this")
        )
        ),
        )
        ,
        (lambda x:x.type=='ambiguous',
        RunnableLambda(lambda x:{"question":"As of today"+x.question})
        |rewrite_chain
        |RunnableLambda(lambda x:{"question":x.question})
        |intent_chain
        |RunnableBranch(
            (
            lambda x:x.intent!="opinion",
            RunnableLambda(lambda x:{"question":x.question,"type":x.intent})
            |answer_chain
            |RunnableLambda(lambda x:{"question":x.question,"answer":x.answer})
            |summary_chain  
            ),
            (
                RunnableLambda(lambda _:"sorry i cant answer to this")
            )
        ),
        ),
        RunnableLambda(lambda _:"this is not valid,it will not be proceeded further")
    )
)


while True:
    query=input("Enter your query: ").lower()
    if query=="exit":
        break
    result=pipeline.invoke({"question":query})
    print(result)