# API Design

The API uses **FastAPI** to provide a strictly-typed, auto-documenting REST interface.
- Swagger UI is available at `/api/docs`.
- Routes are modularized under `api/routes/` for Resources (`projects`, `assets`, `scans`, `findings`, `reports`, `auth`).
- **Websockets** at `/ws` provide real-time pub/sub notifications for EventBus signals.
