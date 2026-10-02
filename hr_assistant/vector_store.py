import os
from  langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from hr_assistant import config
from hr_assistant.embedding import get_embeddings_model
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

# build_vector_store

def build_vector_store(chunks):
    """Embed every chunk and upload it 
    into a Qdrant Cloud Collection."""
    logger.info("Embedding %d chunks and uplopding to Qdrant collection %s", 
                len(chunks),
                config.QDRANT_COLLECTION_NAME,
    )
    embedding_model = get_embeddings_model()
    vector_store= QdrantVectorStore.from_documents(
        chunks,
        embedding= embedding_model,
        url= config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY,
        collection_name= config.QDRANT_COLLECTION_NAME
    )
    logger.info("Uploaded to Qdrant collectgion %s", config.QDRANT_COLLECTION_NAME)
    return vector_store

def load_vector_store():
    """
    Connect to a Qdrant Cloud Collection that was already built before.]
    """
    logger.info("Connecting to Qdrant cloud")
    embeddings_model = get_embeddings_model()
    # allow_dangerous_deserialization is safe here because we only ever load
    # an index that this same app created and saved. 
    return QdrantVectorStore.from_existing_collection(
            embedding= embeddings_model,
            url= config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY,
            collection_name= config.QDRANT_COLLECTION_NAME
        )

def vector_store_exists()->bool:
    """Check if Qdrant store already exists"""
    client= QdrantClient(
        url=config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY
    )
    return client.collection_exists(config.QDRANT_COLLECTION_NAME)

def get_retriver(vector_store, k:int= config.TOP_K_RESULTS):
    """Turn a vector store into a retriver that returns the top-k matching chunks."""
    logger.info("Creating retriever for vector store with top-%d results", k)
    return vector_store.as_retriever(search_kwargs={"k":k})

