from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class EmbedRequest(BaseModel):
    texts: List[str]


class ChatRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None
    top_k: int = 5
    task: str = "regulatory_qa"


class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]