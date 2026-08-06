from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def check_langsmith_tracing()->None:
    """Log whether langsmith tracing is enabled or not."""
    tracing_on = config.LANGSMITH_TRACING.lower() == "true"

    if tracing_on and config.LANGSMITH_API_KEY:
        logger.info("Langsmith tracing is enabled. Endpoint: %s, Project: %s", config.LANGSMITH_ENDPOINT, config.LANGSMITH_PROJECT)

    else:
        logger.info("Langsmith tracing is OFF (set LANGSMITH_TRACING=true and provide LANGSMITH_API_KEY in .env to enable tracing).")