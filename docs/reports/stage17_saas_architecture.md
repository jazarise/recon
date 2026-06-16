# Stage 17: Enterprise Service Architecture

## API Service Layer
ReconX is now fully headless. Execution is completely driven via HTTP REST payloads mapping to `src/reconx/api/server.py`. 

## Authentication & Authorization
The API strictly enforces `Role-Based Access Control`. Tokens must be passed via the `Authorization: Bearer <TOKEN>` header. Viewers cannot trigger new scans, and Admins wield full campaign mutation capabilities.

## Persistent Storage
Memory states have been upgraded to `src/reconx/db/storage.py`, persisting all campaign metadata to a resilient SQLite database, ensuring job states survive container restarts.
