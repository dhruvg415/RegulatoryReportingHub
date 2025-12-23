from app.services.ai_client import AIOrchestratorClient
from app.models.report import Report
import json


class ObligationEngine:
    def __init__(self):
        self.ai = AIOrchestratorClient()

    async def derive_obligations(
        self,
        institution_id: str,
        regulator: str,
        framework: str
    ) -> dict:
        """
        Ask AI to derive obligations using institution-filtered documents.
        """

        prompt = f"""
Identify regulatory obligations for an institution under:

Regulator: {regulator}
Framework: {framework}

Return obligations as structured bullet points.
Each obligation should be explicit and actionable.
"""

        filters = {
            "institution_id": institution_id,
            "regulator": regulator,
            "framework": framework
        }

        response = await self.ai.chat(
            query=prompt,
            filters=filters
        )

        return response


def compute_obligations(institution, db):
    obligations = []

    reports = db.query(Report).all()

    # --- Safely extract threshold criteria ---
    threshold_criteria = institution.threshold_criteria or {}

    if isinstance(threshold_criteria, str):
        try:
            threshold_criteria = json.loads(threshold_criteria)
        except json.JSONDecodeError:
            threshold_criteria = {}

    assets = threshold_criteria.get("total_assets", 0)

    # --- Safely extract entity types ---
    entity_types = institution.legal_entity_types or []

    if isinstance(entity_types, str):
        entity_types = [e.strip().lower() for e in entity_types.split(",")]

    entity_types = [e.lower() for e in entity_types]

    # --- Obligation rules ---
    for report in reports:
        if "bank" in entity_types and assets > 1_000_000_000:
            obligations.append({
                "report_id": report.report_id,
                "report_name": report.name,
                "reason": "Institution is a bank with assets above $1B"
            })

    return obligations