from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.regulator import Regulator
from app.schemas.regulator import RegulatorOut

router = APIRouter(prefix="/regulators", tags=["Regulators"])

@router.get("/", response_model=list[RegulatorOut])
def list_regulators(db: Session = Depends(get_db)):
    return db.query(Regulator).all()

@router.get("/{regulator_id}", response_model=RegulatorOut)
def get_regulator(regulator_id: str, db: Session = Depends(get_db)):
    regulator = db.query(Regulator).filter(
        Regulator.regulator_id == regulator_id
    ).first()

    if not regulator:
        raise HTTPException(status_code=404, detail="Regulator not found")

    return regulator
