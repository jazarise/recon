# Dependency Audit Report

This report defines the cleaned and classified dependencies for ReconX v3.0, verified during Stage 1 Packaging & Installation Audit.

## Required Dependencies
These are essential for the core execution of the ReconX platform:
- `fastapi`
- `pydantic`
- `sqlalchemy`
- `typer`
- `rich`
- `uvicorn`
- `alembic`
- `pyyaml`
- `aiohttp`
- `requests`
- `jinja2`
- `apify-client`
- `beautifulsoup4`
- `python-dotenv`
- `pydantic-settings`
- `questionary`
- `structlog`
- `schedule`
- `aiosqlite`

## Optional Dependencies
These are strictly used for optional modules and specific installation configurations:
- **AI** (`reconx[ai]`): `openai`, `transformers`, `torch`
- **Docs** (`reconx[docs]`): `mkdocs`

## Development Dependencies
These tools are used exclusively for building, testing, and linting the project:
- **Dev** (`reconx[dev]`): `pytest`, `pytest-cov`, `ruff`, `mypy`, `coverage`

## Removed / Unused
- N/A (all remaining packages mapped cleanly to required, ai, docs, or dev extras.)
