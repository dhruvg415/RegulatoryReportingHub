from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Institution(Base):
    __tablename__ = "institutions"

    institution_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    country_of_incorporation = Column(String)
    legal_entity_types = Column(JSON)
    business_lines = Column(JSON)
    products = Column(JSON)
    threshold_criteria = Column(JSON)