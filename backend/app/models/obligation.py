from sqlalchemy import Column, String, Date, JSON, Integer
from app.core.database import Base
import uuid

class Obligation(Base):
    __tablename__ = "obligations"

    obligation_id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )

    institution_id = Column(String, index=True)
    report_id = Column(String, index=True)

    regulator = Column(String)
    framework = Column(String)

    obligation_text = Column(String)
    reason = Column(String)

    source = Column(String)  # "rule" | "ai"
    version = Column(Integer, default=1)

    effective_date = Column(Date)
    metadata = Column(JSON, default={})