from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.institution import Institution
from app.models.obligation import Obligation
from app.models.report import Report
from app.services.obligation_engine import compute_obligations, ObligationEngine

router = APIRouter(prefix="/obligations", tags=["Obligations"])

@router.post("/institutions/{institution_id}/compute")
async def compute_institution_obligations(
    institution_id: str,
    db: Session = Depends(get_db)
):
    institution = db.query(Institution).filter(
        Institution.institution_id == institution_id
    ).first()

    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")

    computed = compute_obligations(institution, db)

    persisted = []

    for ob in computed:
        record = Obligation(
            institution_id=institution_id,
            report_id=ob["report_id"],
            regulator=None,
            framework=None,
            obligation_text=f"File {ob['report_name']}",
            reason=ob["reason"],
            source="rule",
            version=1
        )
        db.add(record)
        persisted.append(record)

    db.commit()

    return {
        "institution_id": institution_id,
        "obligations_created": len(persisted)
    }


@router.post("/institutions/{institution_id}/derive")
async def derive_ai_obligations(
    institution_id: str,
    regulator: str,
    framework: str,
    db: Session = Depends(get_db)
):
    engine = ObligationEngine()
    response = await engine.derive_obligations(
        institution_id=institution_id,
        regulator=regulator,
        framework=framework
    )

    created = []

    for idx, item in enumerate(response.get("answer", "").split("\n")):
        if not item.strip():
            continue

        ob = Obligation(
            institution_id=institution_id,
            regulator=regulator,
            framework=framework,
            obligation_text=item,
            reason="Derived from regulatory text via AI",
            source="ai",
            version=1
        )
        db.add(ob)
        created.append(ob)

    db.commit()

    return {
        "institution_id": institution_id,
        "source": "ai",
        "count": len(created)
    }

@router.get("/institutions/{institution_id}")
def list_obligations(
    institution_id: str,
    db: Session = Depends(get_db)
):
    obs = db.query(Obligation).filter(
        Obligation.institution_id == institution_id
    ).all()

    return obs