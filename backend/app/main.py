from fastapi import FastAPI
from app.routers import (
    regulators,
    reports,
    institutions,
    obligations,
    documents,
    assistant
)

app = FastAPI(title="Regulatory Reporting Hub Backend")

app.include_router(regulators.router)
app.include_router(reports.router)
app.include_router(institutions.router)
app.include_router(obligations.router)
app.include_router(documents.router)
app.include_router(assistant.router)