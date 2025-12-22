from fastapi import APIRouter, Depends
from app.services.ai_client import AIOrchestratorClient
from app.models.institution import Institution
from app.core.database import get_db
from sqlalchemy.orm import Session
from backend.app.schemas import regulator

router = APIRouter(prefix="/assistant", tags=["assistant"])

@router.post("/institutions/{institution_id}/query")
async def ask_about_institution(
    institution_id: str,
    question: str,
    db: Session = Depends(get_db)
):
    institution = db.query(Institution).filter(
        Institution.institution_id == institution_id
    ).first()

    if not institution:
        return {"error": "Institution not found"}

    # Build filters from institution context
    filters = {
        "institution_id": institution.institution_id,
        "jurisdiction": institution.country_of_incorporation,
        "entity_types": institution.legal_entity_types,
        "products": institution.products,
        "regulator": regulator,
    }

    ai_client = AIOrchestratorClient()
    response = await ai_client.chat(
        query=question,
        filters=filters
    )

    return {
        "question": question,
        "answer": response["answer"],
        "sources": response.get("sources", [])
    }