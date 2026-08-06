from hr_assistant import config
from hr_assistant.logger import get_logger

from langchain_groq import ChatGroq

logger = get_logger(__name__)
def get_llm():
    """Return a Groq chat model."""
    logger.info("Initialzing LLM model '%s'", config.LLM_MODEL_NAME)
    return ChatGroq(model=config.LLM_MODEL_NAME, temperature=0)