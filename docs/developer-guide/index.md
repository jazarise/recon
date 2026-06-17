# ReconX Developer Guide

This guide is for engineers looking to contribute to the core ReconX platform. If you only want to write a new plugin, see the [Plugin Development Guide](../plugins/plugin-development.md).

## Project Structure

ReconX uses a Domain-Driven Design (DDD) inspired folder structure:

```text
src/reconx/
├── api/             # FastAPI routes, schemas, and dependencies
├── cli/             # Typer CLI commands
├── config/          # Pydantic Settings and YAML loading
├── core/            # Core business logic
│   ├── asm/         # Asset and Target Management
│   ├── auth/        # JWT Authentication, RBAC, Password hashing
│   ├── database/    # SQLAlchemy models and async session management
│   ├── intelligence/# Correlation, normalization, deduplication
│   ├── plugins/     # Plugin executor and sandbox
│   └── workflow/    # DAG parsing, scheduling, event bus
├── reporting/       # PDF/CSV/HTML/JSON Exporters
├── observability/   # Metrics, tracing, health checks
└── plugins/         # Built-in plugins
```

## Code Style

ReconX enforces a strict coding style validated by CI:
- **Linter**: `ruff`
- **Type Checker**: `mypy` (strict mode where possible)
- **Security Scanner**: `bandit`

Run `ruff check .` and `mypy src` before opening a Pull Request.

## Testing

Testing is non-negotiable. "No bug fix without test."

We use `pytest` with `pytest-asyncio`. 
Tests are located in `tests/`.

```bash
pytest
```

## Dependency Injection

ReconX heavily relies on FastAPI's `Depends` for request scoping, particularly around the database session.
Core services should be designed to accept dependencies (like `AsyncSession`) rather than creating them directly.
