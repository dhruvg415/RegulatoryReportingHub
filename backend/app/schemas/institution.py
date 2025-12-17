from pydantic import BaseModel
from typing import List, Dict
from uuid import UUID

class InstitutionCreate(BaseModel):
    name: str
    country_of_incorporation: str
    legal_entity_types: List[str]
    business_lines: List[str]
    products: List[str]
    threshold_criteria: Dict

class InstitutionOut(InstitutionCreate):
    institution_id: UUID

    class Config:
        orm_mode = True