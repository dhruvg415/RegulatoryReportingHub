from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    regulator = Column(String, nullable=False)
    framework = Column(String, nullable=True)
    jurisdiction = Column(String, nullable=True)

    source_url = Column(String, nullable=True)
    raw_text = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())