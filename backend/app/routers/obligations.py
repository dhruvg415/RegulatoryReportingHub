from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.institution import Institution
from app.services.obligation_engine import compute_obligations

router = APIRouter(prefix="/obligations", tags=["Obligations"])

@router.post("/institutions/{institution_id}/compute")
def compute_institution_obligations(
    institution_id: str,
    db: Session = Depends(get_db)
):
    institution = db.query(Institution).filter(
        Institution.institution_id == institution_id
    ).first()

    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")

    obligations = compute_obligations(institution, db)

    return {
        "institution_id": institution_id,
        "obligations": obligations
    }