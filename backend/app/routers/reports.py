from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.report import Report
from app.schemas.report import ReportOut

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/", response_model=list[ReportOut])
def list_reports(
    framework_id: str | None = Query(default=None),
    regulator_id: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Report)

    if framework_id:
        query = query.filter(Report.framework_id == framework_id)

    if regulator_id:
        query = query.filter(Report.issuing_regulator_id == regulator_id)

    return query.all()

@router.get("/{report_id}", response_model=ReportOut)
def get_report(report_id: str, db: Session = Depends(get_db)):
    report = db.query(Report).filter(
        Report.report_id == report_id
    ).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report
