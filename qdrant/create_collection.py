from qdrant_client.http import models

def create_collection(client, collection_name):
    first_collection = client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=384, distance=models.Distance.COSINE)
    )
    return first_collection

