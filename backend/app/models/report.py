import uuid
from sqlalchemy import Column, String, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Report(Base):
    __tablename__ = "reports"

    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    code = Column(String, nullable=True)

    issuing_regulator_id = Column(UUID(as_uuid=True), nullable=False)
    framework_id = Column(UUID(as_uuid=True), nullable=True)

    purpose = Column(String)
    frequency = Column(String)
    due_date_pattern = Column(String)

    submission_channels = Column(ARRAY(String))
    filing_entity_types = Column(ARRAY(String))
    formats = Column(ARRAY(String))