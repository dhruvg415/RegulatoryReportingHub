from fastapi import FastAPI
from app.schemas import EmbedRequest, ChatRequest, ChatResponse
from app.clients.azure_openai import embed_text, chat
from app.clients.qdrant import init_collection, upsert_chunk, search
import uuid
import os

app = FastAPI(title="AI Orchestrator")

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