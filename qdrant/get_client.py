
from qdrant_client import QdrantClient
from utils.constants import QDRANT_API_KEY, QDRANT_URL


def get_client():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    return client
