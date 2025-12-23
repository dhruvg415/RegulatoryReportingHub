from pydantic import BaseModel
from datetime import date
from uuid import UUID
from typing import List, Optional, Dict

class ObligationBase(BaseModel):
    institution_id: UUID
    regulator: str
    framework: str
    title: str
    description: str
    effective_date: date

class ObligationCreate(ObligationBase):
    pass

class ObligationOut(ObligationBase):
    obligation_id: UUID
    rationale: Optional[str]
    sources: Optional[List[Dict]]
    status: str

    class Config:
        from_attributes = True