from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class RegulatorOut(BaseModel):
    regulator_id: UUID
    name: str
    jurisdiction: str
    regulatory_domains: Optional[List[str]]
    official_website: Optional[str]

    class Config:
        from_attributes = True