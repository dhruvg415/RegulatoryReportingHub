from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.institution import InstitutionCreate, InstitutionOut
from app.models.institution import Institution
from app.core.database import get_db

router = APIRouter(prefix="/institutions", tags=["Institutions"])

@router.post("/", response_model=InstitutionOut)
def create_institution(data: InstitutionCreate, db: Session = Depends(get_db)):
    inst = Institution(**data.dict())
    db.add(inst)
    db.commit()
    db.refresh(inst)
    return inst