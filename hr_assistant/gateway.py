import json

from langchain_openai import ChatOpenAI
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)


#model routing

PRIMARY_TARGET = {
    "provider":"@hrpolicy",
    "override_params": {"model": config.LLM_MODEL_NAME}
}

#backup model
FALLBACK_TARGET = {
    "provider":"@hrpolicybackup",
    "override_params": {"model":"openai/gpt-oss-20b"}
}

# gateway features
# loadbalancing
# model routing
# caching
# fallback

# to use these features we use :- config (SET OF RULES)

#public -- anyone can edit
#private 

GATEWAY_CONFIG = {
    "strategy":{
        "mode":"fallback"
    },
    "targets": [PRIMARY_TARGET, FALLBACK_TARGET]
}


def get_gateway_llm() -> ChatOpenAI:
    """return a chat model routed through Portkey, with automatic model fallback"""
    logger.info("Routing LLM calls through Portkey (primary=@hrpolicy, fallback=@hrpolicybackup)")
    headers = createHeaders(api_key=config.PORTKEY_API_KEY,
                            config="pc-hrpoli-d6580c")
                            # config=json.dumps(GATEWAY_CONFIG))
    return ChatOpenAI(
        api_key="dummy",
        base_url=PORTKEY_GATEWAY_URL,
        default_headers=headers
    )