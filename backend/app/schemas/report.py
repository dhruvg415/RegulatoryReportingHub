from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ReportOut(BaseModel):
    report_id: UUID
    name: str
    code: Optional[str]
    frequency: Optional[str]
    due_date_pattern: Optional[str]
    submission_channels: Optional[List[str]]
    filing_entity_types: Optional[List[str]]
    formats: Optional[List[str]]

    class Config:
        from_attributes = True