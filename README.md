# Brahma Slides

Brahma Slides is an IR-first presentation platform. Phase 0 provides a manual presentation editor foundation: a FastAPI API persists and validates Presentation IR, and a deterministic renderer exports editable PPTX files. No AI generation is implemented.

## Quick start

1. Copy `.env.example` to `.env` and start PostgreSQL: `docker compose up -d postgres`.
2. Start the API: `cd apps/api && python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/uvicorn app.main:app --reload`.
3. Start the web app: `cd apps/web && npm install && npm run dev`.

The API is available at `http://localhost:8000`, with OpenAPI documentation at `/docs`. The editor is available at `http://localhost:3000`.

## Local AI API

The backend is configured for a **local-only OpenAI-compatible LocalAI API**, not a cloud provider. Start LocalAI on `http://localhost:8080/v1` (or set `LOCAL_AI_BASE_URL` and `LOCAL_AI_MODEL` in `.env`) and check connectivity at `GET /api/v1/ai/status`. The Phase 0 API permits only loopback/host-local endpoints and does not yet send prompts or generate slides; this provider boundary is reserved for Phase 1.

For the local test suite use `cd apps/api && python -m pytest`. Tests use SQLite and do not require Docker.

See [architecture](docs/architecture.md), [Presentation IR](docs/presentation-ir.md), [API](docs/api.md), and [development](docs/development.md).
