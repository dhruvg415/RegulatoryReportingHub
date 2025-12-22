from pydantic import BaseModel
from typing import Optional

class DocumentCreate(BaseModel):
    id: str
    title: str
    regulator: str
    framework: Optional[str] = None
    jurisdiction: Optional[str] = None
    source_url: Optional[str] = None
    raw_text: Optional[str] = None


class DocumentOut(BaseModel):
    id: str
    title: str
    regulator: str
    framework: Optional[str]
    jurisdiction: Optional[str]

    class Config:
        orm_mode = True
