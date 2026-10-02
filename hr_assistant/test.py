from qdrant_client import QdrantClient
from hr_assistant import config


client= QdrantClient(
        url=config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY
    )

print(client.get_collections())