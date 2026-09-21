# Brahma Slides

Brahma Slides is an IR-first presentation platform. Phase 0 provides a manual editor foundation: a FastAPI API persists and validates Presentation IR, and a deterministic renderer exports editable PowerPoint files. **No AI generation is implemented.**

Phase 0 includes Presentation IR validation, PostgreSQL persistence with version snapshots, a Next.js manual editor, editable PPTX export, and a local-only AI connectivity boundary.

## Quick start

### PostgreSQL

```bash
cp .env.example .env
docker compose up -d postgres
```

### API (Linux/macOS)

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### API (Windows PowerShell)

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The API is at `http://localhost:8000`; OpenAPI documentation is at `http://localhost:8000/docs`.

### Web editor

```bash
cd apps/web
npm install
npm run dev
```

Open `http://localhost:3000`. Create a presentation, add/reorder slides, add/edit/move/resize text and shapes, upload a local image, save/reload, and export editable PPTX.

### Tests

```bash
cd apps/api
python -m pytest
```

Tests use SQLite and do not require Docker.

## Local AI API

The backend is configured for a **local-only OpenAI-compatible LocalAI API**, not a cloud provider. Its default is `http://localhost:8080/v1`; configure `LOCAL_AI_BASE_URL` and `LOCAL_AI_MODEL` in `.env` when needed.

`GET /api/v1/ai/status` checks only the local server’s `/models` connectivity. Phase 0 permits loopback/host-local endpoints only and never sends prompts or generates slides. That pipeline belongs to Phase 1.

See [architecture](docs/architecture.md), [Presentation IR](docs/presentation-ir.md), [API](docs/api.md), and [development](docs/development.md).
