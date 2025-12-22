from qdrant_client import QdrantClient
from qdrant_client.http import models
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


def search(
    query_vector,
    top_k: int = 6,
    filters: dict | None = None
):
    qdrant_filters = None

    if filters:
        must_conditions = []

        for key, value in filters.items():
            if isinstance(value, list):
                must_conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchAny(any=value)
                    )
                )
            else:
                must_conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    )
                )

        qdrant_filters = models.Filter(must=must_conditions)

    return client.search(
        collection_name=COLLECTION,
        query_vector=query_vector,
        limit=top_k,
        query_filter=qdrant_filters
    )
