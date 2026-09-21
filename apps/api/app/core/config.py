from pathlib import Path
import os
from urllib.parse import urlparse


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./brahma_slides.db")
STORAGE_PATH = Path(os.getenv("STORAGE_PATH", "./exports"))
LOCAL_AI_BASE_URL = os.getenv("LOCAL_AI_BASE_URL", "http://localhost:8080/v1").rstrip("/")
LOCAL_AI_MODEL = os.getenv("LOCAL_AI_MODEL", "local-model")


def validate_local_ai_url(url: str = LOCAL_AI_BASE_URL) -> str:
    """Allow only a loopback LocalAI/OpenAI-compatible endpoint in Phase 0."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {"localhost", "127.0.0.1", "::1", "host.docker.internal"}:
        raise ValueError("LOCAL_AI_BASE_URL must point to a local hostname")
    return url.rstrip("/")
