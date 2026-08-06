import os
from  langchain_community.vectorstores import FAISS
from hr_assistant import config
from hr_assistant.embedding import get_embeddings_model
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

# build_vector_store

def build_vector_store(chunks):
    """Embed every chunk and build a searchable FAISS index in memory."""
    logger.info("Embedding %d chunks and building FAISS index", len(chunks))
    embedding_model = get_embeddings_model()
    vector_store= FAISS.from_documents(chunks, embedding_model)
    logger.info("FAISS index built successfully")
    return vector_store

# save_vector_store

def save_vector_store(vector_store, path: str = config.VECTOR_STORE_PATH)->None:
    """Save the FAISS index to disk so we don't have to rebuild it every time."""
    logger.info("Saving FAISS index to disk at '%s'", path)
    vector_store.save_local(path)
    logger.info("FAISS index saved successfully")

# load_vector_store

def load_vector_store(path: str = config.VECTOR_STORE_PATH):
    """Load previously build FAISS from disk"""
    logger.info("Loading FAISS index from disk at '%s'", path)
    embeddings_model = get_embeddings_model()
    # allow_dangerous_deserialization is safe here because we only ever load
    # an index that this same app created and saved. 
    return FAISS.load_local(path, embeddings_model, allow_dangerous_deserialization= True)

def vector_store_exists(path:str= config.VECTOR_STORE_PATH)->bool:
    """Check if a saved FAISS index already exists on disk"""
    logger.info("Checking if FAISS index exists at '%s'", path)
    return os.path.exists(os.path.join(path, "index.faiss"))

def get_retriver(vector_store, k:int= config.TOP_K_RESULTS):
    """Turn a vector store into a retriver that returns the top-k matching chunks."""
    logger.info("Creating retriever for vector store with top-%d results", k)
    return vector_store.as_retriever(search_kwargs={"k":k})

