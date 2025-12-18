from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import os

client = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333")
)

COLLECTION = "regulatory_documents"


def init_collection(vector_size: int):
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION not in collections:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )


def upsert_chunk(point_id: str, vector: list[float], payload: dict):
    client.upsert(
        collection_name=COLLECTION,
        points=[{
            "id": point_id,
            "vector": vector,
            "payload": payload
        }]
    )


def search(vector: list[float], top_k: int):
    return client.search(
        collection_name=COLLECTION,
        query_vector=vector,
        limit=top_k
    )
