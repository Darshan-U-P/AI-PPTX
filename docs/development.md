# Development

Use Python 3.12+ and Node 20+. `docker compose up -d postgres` starts the development database. Set `DATABASE_URL` to the PostgreSQL connection string in `.env`; if omitted, the API uses a local SQLite file for simple development.

Run backend checks with `cd apps/api && python -m pytest`. Run frontend checks with `cd apps/web && npx tsc --noEmit && npm run build`. The API creates tables during startup in Phase 0; migrations can be introduced before production deployment.

To use the local AI API boundary, run a LocalAI/OpenAI-compatible service on `http://localhost:8080/v1`, then call `GET http://localhost:8000/api/v1/ai/status`. The endpoint is intentionally restricted to local hostnames and only checks `/models`; it does not perform generation in Phase 0.
