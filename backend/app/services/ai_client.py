import httpx
from app.core.config import settings

class AIOrchestratorClient:
    def __init__(self):
        self.base_url = settings.AI_ORCHESTRATOR_URL

    async def chat(self, query: str, filters: dict | None = None):
        payload = {
            "query": query,
            "filters": filters or {},
            "top_k": 6
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self.base_url}/chat",
                json=payload
            )
            resp.raise_for_status()
            return resp.json()