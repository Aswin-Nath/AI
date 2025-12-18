import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json
GROQ_KEY=os.getenv("GROQ_API_KEY")
# Initialize Groq LLM
model="llama-3.1-8b-instant"
llm = ChatGroq(
    api_key=GROQ_KEY,
    model_name=model,
    temperature=0
)
