from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentOut

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("/", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

@router.get("/{document_id}", response_model=DocumentOut)
def get_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(
        Document.document_id == document_id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc
