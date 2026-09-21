from fastapi import APIRouter

from app.services.local_ai_service import LocalAIService

router = APIRouter(prefix="/ai", tags=["local-ai"])


@router.get("/status")
async def local_ai_status():
    """Report whether the configured localhost LocalAI endpoint is available.

    This is intentionally a connectivity boundary only; presentation generation is
    deferred until Phase 1.
    """
    return await LocalAIService().status()
