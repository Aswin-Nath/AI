from langchain_ollama import ChatOllama
llm = ChatOllama(
    model="mistral",          # change to the model you installed
    temperature=0.7,
)
