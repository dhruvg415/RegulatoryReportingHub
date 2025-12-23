from sqlalchemy import Column, String, Date, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class Obligation(Base):
    __tablename__ = "obligations"

    obligation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    institution_id = Column(UUID(as_uuid=True), ForeignKey("institutions.institution_id"), nullable=False)

    regulator = Column(String, nullable=False)
    framework = Column(String, nullable=False)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    effective_date = Column(Date, nullable=False)

    # AI explainability
    rationale = Column(Text, nullable=True)
    sources = Column(JSON, nullable=True)

    # Optional status tracking
    status = Column(String, default="active")  # active | superseded | deprecated