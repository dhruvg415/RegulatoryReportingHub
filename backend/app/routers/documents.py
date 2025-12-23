from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.document import DocumentCreate, DocumentOut
from app.models.document import Document
from app.core.database import get_db
from app.services.ai_client import AIOrchestratorClient

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/documents/{document_id}/ingest")
async def ingest_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(
        Document.document_id == document_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    ai_client = AIOrchestratorClient()

    result = await ai_client.ingest(
        file_path=document.file_path,
        institution_id=document.institution_id,
        metadata={
            "regulator": document.regulator,
            "framework": document.framework,
            "effective_date": document.effective_date.isoformat(),
            "document_id": document.document_id,
            "version": document.version
        }
    )

    return result

