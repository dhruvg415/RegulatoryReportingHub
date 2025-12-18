from pydantic import BaseModel
from datetime import date
from typing import Optional, Dict
from uuid import UUID

class DocumentOut(BaseModel):
    document_id: UUID
    title: str
    type: str
    jurisdiction: str
    effective_date: Optional[date]
    status: str
    storage_path: str
    metadata: Dict

    class Config:
        from_attributes = True
