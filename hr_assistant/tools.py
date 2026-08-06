from langchain.tools import tool

def create_search_tool(retriver):
    """Return @tool function that searches the HR policy document"""

    @tool
    def search_hr_policy(question:str)->str:
        """ search the HR policy document for leave, work form home, probation,
            notice period, reimbursement, code of conduct, holiday or exit process"""
        matching_chunks = retriver.invoke(question)
        return "\n\n".join(chunk.page_content for chunk in matching_chunks)

    return search_hr_policy