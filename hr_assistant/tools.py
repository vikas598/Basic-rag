from langchain.tools import tool
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def create_search_tool(retriver):
    """Return @tool function that searches the HR policy document"""

    @tool
    def search_hr_policy(question:str)->str:
        """ search the HR policy document for leave, work form home, probation,
            notice period, reimbursement, code of conduct, holiday or exit process"""
        logger.info("serch_hr_policy tool invoked with question: %s", question)
        matching_chunks = retriver.invoke(question)
        logger.info("Found %d matching chunks", len(matching_chunks))
        return "\n\n".join(chunk.page_content for chunk in matching_chunks)

    return search_hr_policy