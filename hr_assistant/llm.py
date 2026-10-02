from hr_assistant.logger import get_logger

from hr_assistant.gateway import get_gateway_llm

logger = get_logger(__name__)

def get_llm():
    """Return a Groq chat model."""
    logger.info("Initialzing LLM via portkey")
    return get_gateway_llm()