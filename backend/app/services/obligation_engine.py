def compute_obligations(institution, reports):
    obligations = []

    for report in reports:
        # simple rule: banks with assets > 1bn must file
        assets = institution.threshold_criteria.get("total_assets", 0)

        if "bank" in institution.legal_entity_types and assets > 1_000_000_000:
            obligations.append({
                "report_id": report.report_id,
                "reason": "Institution is a bank with assets above threshold"
            })

    return obligations