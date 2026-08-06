import os
from dotenv import load_dotenv

load_dotenv()

## ENV VARIABLE

GROQ_API_KEY= os.getenv("GROQ_API_KEY")
JINA_API_KEY= os.getenv("JINA_API_KEY")


# TRACING

LANGSMITH_TRACING= os.getenv("LANGSMITH_TRACING", "false")
LANGSMITH_ENDPOINT= os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY= os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT= os.getenv("LANGSMITH_PROJECT")

## DEFINE PATH- DATA/VECTOR STORE

DATA_FILE_PATH = os.path.join("data", "hr_policy.txt")

## VECTOR STORES
# IN MEMORY
# PERSISTANT MEMORY - vector # 100GB - ingestion
# CLOUD MEMORY

VECTOR_STORE_PATH = os.path.join("data","faiss_index")

##  MODELS
# LLM AND EMBEDDING MODEL

LLM_MODEL_NAME = "openai/gpt-oss-20b"

EMBEDDING_MODEL_NAME = "jina-embeddings-v2-base-en"

## CHUNK/ TEXT SPLITTING CONFIGS

CHUNK_SIZE=500
CHUNK_OVERLAP = 50

# RETRIVAL RESULTS
TOP_K_RESULTS = 3

## SYSTEM INSTRUCTIONS

SYSTEM_PROMPT="""
    You are a friendly HR assistant working for Acmecrop.
    Always use the search_hr_policy tool to look up facta before answering .
    If the answer isn't in the search results, say you don't know "instead of guessing".
    """

def check_api_keys() -> None:
    """Stop early if the API key is missing"""
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ api key.")
    if not JINA_API_KEY:
        raise ValueError("Missing JINA api key.")