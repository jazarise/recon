# Feature Freeze

## Features Included
- Native Python Modules (Subfinder, Nmap, Naabu, HTTPX via native binaries or APIs)
- Topological Workflow Engine
- HTMX Dashboard
- FastAPI REST Service
- Correlation & Deduplication Engine
- Asset Risk Engine
- Reporting Engine (HTML, JSON, CSV, Markdown)
- CI/CD Pipelines

## Features Deferred
- Multi-user collaboration (Moved to v3.0)
- Distributed cloud scanning workers (Moved to v3.0)
- Plugin marketplace (Moved to v2.2)

## Known Limitations
- The correlation graph generates raw JSON; a visual frontend node graph is pending.
- SQLite is the only officially supported backend right now.
