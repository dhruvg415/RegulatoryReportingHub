import uuid
from sqlalchemy import Column, String, Date, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    document_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # rulebook, ITS, RTS, guideline, etc.
    jurisdiction = Column(String, nullable=False)

    source_regulator_id = Column(UUID(as_uuid=True), nullable=True)
    framework_id = Column(UUID(as_uuid=True), nullable=True)

    effective_date = Column(Date, nullable=True)
    status = Column(String, default="Active")

    storage_path = Column(String, nullable=False)  # MinIO / S3 path
    metadata = Column(JSON, default=dict)