from fastapi import FastAPI

app = FastAPI(title="Regulatory Reporting Hub")

@app.get("/health")
def health():
    return {"status": "ok"}