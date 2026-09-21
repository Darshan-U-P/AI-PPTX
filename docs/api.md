# API

All routes are versioned below `/api/v1`. Presentation CRUD is available at `/presentations`; slide CRUD is available at `/presentations/{presentation_id}/slides` and `/slides/{slide_id}`. `POST /presentations/{id}/validate` returns the validated IR, and `POST /presentations/{id}/export` streams an editable `.pptx` attachment.

Errors use `{ "error": { "code": "…", "message": "…" } }`. Validation failures return HTTP 422 with FastAPI field details; missing resources return HTTP 404.

`GET /ai/status` checks the configured localhost LocalAI/OpenAI-compatible server's `/models` endpoint. It returns provider, endpoint, configured model, availability, and locally available model IDs. It does not make generation requests.
