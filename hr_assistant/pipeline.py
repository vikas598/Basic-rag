from hr_assistant import config
from hr_assistant.agent import create_hr_agent
from hr_assistant.document_loader import load_document 
from hr_assistant.llm import get_llm
from hr_assistant.splitter import split_into_chunks
from hr_assistant.tools import create_search_tool
from hr_assistant.vector_store import (
    build_vector_store,
    save_vector_store,
    get_retriver,
    load_vector_store,
    vector_store_exists
)
from hr_assistant.logger import get_logger
from hr_assistant.tracing import check_langsmith_tracing
from hr_assistant.guardrails import check_input, check_output, REFUSAL_MSG

logger = get_logger(__name__)

def build_vector_store_for_document(file_path: str = config.DATA_FILE_PATH):
    """Load + split+ embed the document, resuing a saved index if we have one"""
    if vector_store_exists():
        print("Found a saved vector store on disk, loading it (fast, no re-embedding).")
        logger.info("Found a saved vector store on disk, reusing it.")
        return load_vector_store()

    print("No saved vector store found, building one from scratch...")
    logger.info("No saved vector store found, building one from scratch from '%s'", file_path)
    documents = load_document(file_path)
    chunks= split_into_chunks(documents)
    print(f"Loaded '{file_path}' and split it into {len(chunks)} chunks.")

    vector_store= build_vector_store(chunks)
    save_vector_store(vector_store)
    print("Vector store build and saved to disk for the next time")
    return vector_store

def build_hr_assistant(file_path:str = config.DATA_FILE_PATH):
    """Build the full RAG agent, ready to answer questions."""
    logger.info("Building HR assistant from document '%s'", file_path)
    config.check_api_keys()
    check_langsmith_tracing()

    vector_store = build_vector_store_for_document(file_path)
    retriver = get_retriver(vector_store)
    search_tool= create_search_tool(retriver)

    llm = get_llm()
    agent = create_hr_agent(llm, [search_tool])

    logger.info("HR assistant built successfully and ready to answer questions")
    return agent

def ask(agent, question:str)->str:
    """Ask the agent a question and return a final answer as plain text. """
    logger.info("Asking agent question: %s", question)

    # input gurad to get safe inputs

    input_is_safe, _ = check_input(question)
    if not input_is_safe:
        return REFUSAL_MSG

    response = agent.invoke({"messages":[{"role":"user","content": question}]})
    answer= response['messages'][-1].content
    logger.info("Final answer from agent: %s", answer)

    # output guard - to check if agent gives safe answer
    output_is_safe, _ = check_output(answer)
    if not output_is_safe:
        return REFUSAL_MSG

    return answer

