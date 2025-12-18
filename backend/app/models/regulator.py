import uuid
from sqlalchemy import Column, String, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Regulator(Base):
    __tablename__ = "regulators"

    regulator_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    jurisdiction = Column(String, nullable=False)

    regulatory_domains = Column(ARRAY(String))
    official_website = Column(String)

    rulebook_sources = Column(JSON, default=list)