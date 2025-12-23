from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentOut
from app.services.ai_client import AIOrchestratorClient
import uuid
import os

router = APIRouter(prefix="/documents", tags=["Documents"])


UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=DocumentOut)
async def upload_document(
    institution_id: str = Form(...),
    regulator_id: str = Form(...),
    framework_id: str = Form(...),
    title: str = Form(...),
    effective_date: str | None = Form(None),
    version: str | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save file
    filename = f"{uuid.uuid4()}_{file.filename}"
    storage_path = os.path.join(UPLOAD_DIR, filename)

    with open(storage_path, "wb") as f:
        f.write(await file.read())

    # Create document record
    doc = Document(
        institution_id=institution_id,
        regulator_id=regulator_id,
        framework_id=framework_id,
        title=title,
        filename=file.filename,
        storage_path=storage_path,
        effective_date=effective_date,
        version=version
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Trigger ingestion
    ai_client = AIOrchestratorClient()
    await ai_client.ingest(
        file_path=storage_path,
        institution_id=institution_id,
        metadata={
            "document_id": doc.document_id,
            "regulator_id": regulator_id,
            "framework_id": framework_id,
            "effective_date": effective_date,
            "version": version
        }
    )

    return doc