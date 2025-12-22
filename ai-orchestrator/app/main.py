from fastapi import FastAPI
from app.schemas import EmbedRequest, ChatRequest, ChatResponse
from app.clients.azure_openai import embed_text, chat
from app.clients.qdrant import init_collection, upsert_chunk, search
from app.ingestion.parser import parse_document
from app.ingestion.chunker import chunk_text
from pydantic import BaseModel
import uuid
import os

app = FastAPI(title="AI Orchestrator")

class IngestRequest(BaseModel):
    file_path: str
    metadata: dict | None = None

# Initialize vector collection on startup
@app.on_event("startup")
def startup():
    # text-embedding-3-large → 3072 dims
    init_collection(vector_size=3072)


@app.post("/embed")
def embed(req: EmbedRequest):
    results = []
    for text in req.texts:
        vector = embed_text(text)
        point_id = str(uuid.uuid4())
        upsert_chunk(
            point_id,
            vector,
            {"text": text}
        )
        results.append({"id": point_id})
    return {"status": "ok", "points": results}


@app.post("/chat", response_model=ChatResponse)
def rag_chat(req: ChatRequest):
    query_vector = embed_text(req.query)
    hits = search(query_vector, req.top_k)

    context_blocks = []
    sources = []

    for h in hits:
        context_blocks.append(h.payload["text"])
        sources.append({
            "id": h.id,
            "score": h.score
        })

    system_prompt_path = f"app/prompts/{req.task}.txt"
    system_prompt = open(system_prompt_path).read()

    user_prompt = f"""
Context:
{chr(10).join(context_blocks)}

Question:
{req.query}
"""

    answer = chat(system_prompt, user_prompt)

    return ChatResponse(
        answer=answer,
        sources=sources
    )


@app.post("/ingest")
def ingest_document(req: IngestRequest):
    """
    End-to-end ingestion:
    file -> text -> chunks -> embeddings -> qdrant
    """

    if not os.path.exists(req.file_path):
        return {"error": "File not found"}

    filename = os.path.basename(req.file_path)

    # Read file bytes
    with open(req.file_path, "rb") as f:
        file_bytes = f.read()

    # Parse document
    parsed = parse_document(file_bytes, filename)
    full_text = parsed["full_text"]

    if not full_text:
        return {"error": "No extractable text found"}

    # Chunk text
    chunks = chunk_text(full_text)

    inserted_points = []

    # Embed + store each chunk
    for chunk in chunks:
        vector = embed_text(chunk["text"])
        point_id = str(uuid.uuid4())

        payload = {
            "text": chunk["text"],
            "chunk_index": chunk["chunk_index"],
            "token_count": chunk["token_count"],
            "source_file": filename,
            **(req.metadata or {})
        }

        upsert_chunk(point_id, vector, payload)
        inserted_points.append(point_id)

    return {
        "status": "ingested",
        "chunks": len(chunks),
        "points": inserted_points
    }