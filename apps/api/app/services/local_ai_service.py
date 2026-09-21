"""Local-only OpenAI-compatible provider boundary for future presentation agents."""

import httpx

from app.core.config import LOCAL_AI_BASE_URL, LOCAL_AI_MODEL, validate_local_ai_url


class LocalAIService:
    """Talks only to a locally hosted OpenAI-compatible API (for example LocalAI)."""

    def __init__(self, base_url: str = LOCAL_AI_BASE_URL, model: str = LOCAL_AI_MODEL):
        self.base_url = validate_local_ai_url(base_url)
        self.model = model

    async def status(self) -> dict[str, object]:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{self.base_url}/models")
                response.raise_for_status()
            payload = response.json()
            models = [item.get("id", "unknown") for item in payload.get("data", []) if isinstance(item, dict)]
            return {"available": True, "provider": "local", "base_url": self.base_url, "model": self.model, "models": models}
        except httpx.HTTPError:
            return {"available": False, "provider": "local", "base_url": self.base_url, "model": self.model, "models": [], "reason": "connection_failed"}
