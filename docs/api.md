# API

All routes are versioned below `/api/v1`. Presentation CRUD is available at `/presentations`; slide CRUD is available at `/presentations/{presentation_id}/slides` and `/slides/{slide_id}`. `POST /presentations/{id}/validate` returns the validated IR, and `POST /presentations/{id}/export` streams an editable `.pptx` attachment.

Errors use `{ "error": { "code": "…", "message": "…" } }`. Validation failures return HTTP 422 with FastAPI field details; missing resources return HTTP 404.

`GET /ai/status` checks the configured localhost LocalAI/OpenAI-compatible server's `/models` endpoint. A successful response includes `{ "available": true, "provider": "local", "base_url", "model", "models" }`; an unavailable server returns `available: false` and `reason: "connection_failed"`. It does not make generation requests.
