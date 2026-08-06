from hr_assistant import config

from langchain_groq import ChatGroq

def get_llm():
    """Return a Groq chat model."""
    return ChatGroq(model=config.LLM_MODEL_NAME, temperature=0)