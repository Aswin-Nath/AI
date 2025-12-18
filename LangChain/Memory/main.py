# sql_related imports
from langchain_community.utilities import SQLDatabase
from dataclasses import dataclass
from Models.groq import llm
# langchain related imports
from langchain.tools import tool
from langchain.agents import create_agent
import os
from dotenv import load_dotenv
load_dotenv()
db_url=os.getenv("POSTGRES_URL")
db=SQLDatabase.from_uri(db_url)

@dataclass
class RuntimeContext:
    db:SQLDatabase

schema_info = db.get_table_info()

print(schema_info)

# ===============================
# System Prompt
# ===============================
SYSTEM_PROMPT = f"""
You are a careful SQLite analyst.

Database schema (authoritative — do NOT guess anything not listed):

{schema_info}

Rules:
- You MUST ONLY use the tables and columns listed above.
- Do NOT invent table or column names.
- When data is needed, call the tool `execute_sql` with ONE SELECT query.
- Use JOINs where required.
- Read-only queries only.
- Limit to 5 rows unless explicitly asked.
- Prefer explicit column lists.
- If a query fails, fix it USING THE SCHEMA ABOVE.
"""

def execute_query(db):
    @tool
    def perform_query(query:str):
        """
        This is will peform db operations 
        
        :param query: Description
        :type query: str
        """
        try:
            return db.run(query)
        except Exception as e:
            return f"Error occured ${e}"
    
    return perform_query
execute=execute_query(db)
agent=create_agent(llm,tools=[execute],system_prompt=SYSTEM_PROMPT,context_schema=RuntimeContext)


question = "This is Frank Harris, What was the total on my last invoice?"

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
    context=RuntimeContext(db=db),
):
    step["messages"][-1].pretty_print()
