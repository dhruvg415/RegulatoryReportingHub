import os

class Settings:
    AI_ORCHESTRATOR_URL: str = os.getenv(
        "AI_ORCHESTRATOR_URL",
        "http://ai-orchestrator:8100"
    )

settings = Settings()