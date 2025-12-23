from sqlalchemy import Column, String, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class Document(Base):
    __tablename__ = "documents"

    document_id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    institution_id = Column(
        String,
        ForeignKey("institutions.institution_id"),
        nullable=False
    )

    regulator_id = Column(
        String,
        ForeignKey("regulators.regulator_id"),
        nullable=False
    )

    framework_id = Column(
        String,
        ForeignKey("frameworks.framework_id"),
        nullable=False
    )

    title = Column(String, nullable=False)
    filename = Column(String, nullable=False)

    effective_date = Column(Date, nullable=True)
    version = Column(String, nullable=True)

    storage_path = Column(String, nullable=False)

    extra_metadata = Column(JSON, nullable=True)

    # Relationships (optional but useful later)
    institution = relationship("Institution")
    regulator = relationship("Regulator")
    framework = relationship("Framework")