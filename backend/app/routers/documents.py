from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.document import DocumentCreate, DocumentOut
from app.models.document import Document
from app.core.database import get_db
from app.services.ai_client import AIOrchestratorClient

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/", response_model=DocumentOut)
async def create_document(
    data: DocumentCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Document).filter(Document.id == data.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Document already exists")

    doc = Document(**data.dict())
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # 🔹 Trigger ingestion in AI Orchestrator
    ai_client = AIOrchestratorClient()
    await ai_client.ingest_document(
        document_id=doc.id,
        text=data.raw_text,
        metadata={
            "regulator": data.regulator,
            "framework": data.framework,
            "jurisdiction": data.jurisdiction,
            "title": data.title
        }
    )

    return doc
