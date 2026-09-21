# Architecture

Phase 0 is a modular monorepo. `packages/schema` defines the canonical Presentation IR contract. `apps/api` validates and persists that contract, while `services/renderer` transforms it into an editable PPTX. The web editor reads and mutates the same IR over REST; it does not maintain a renderer-specific slide model.

The renderer has no API, database, or AI dependencies. Future model providers and agents must produce controlled IR commands rather than files. The only model boundary currently present is `LocalAIService`, which uses a configured local OpenAI-compatible LocalAI endpoint and exposes connectivity status only—there is no generation logic in Phase 0. PostgreSQL is the production datastore; SQLite is supported only for deterministic local tests.
