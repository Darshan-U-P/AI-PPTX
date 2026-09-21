import pytest

from app.core.config import validate_local_ai_url
from app.services.local_ai_service import LocalAIService


def test_local_ai_rejects_nonlocal_endpoint():
    with pytest.raises(ValueError, match="local hostname"):
        validate_local_ai_url("https://api.openai.com/v1")


def test_local_ai_status_handles_unavailable_server():
    status = __import__("asyncio").run(LocalAIService(base_url="http://localhost:9/v1").status())
    assert status["reachable"] is False
    assert status["models"] == []
