# ReconX Dependency Audit
*Generated during Repository Cleanup - Phase 21*

## 1. Used Dependencies (Core Platform)
These are actively used in the current Linux-native Enterprise architecture:
- `fastapi>=0.111` (Core API)
- `uvicorn[standard]>=0.30` (ASGI Server)
- `PyYAML>=6.0` (Workflow Engine)
- `SQLAlchemy>=2.0.0` (Asset Database)
- `APScheduler>=3.10.1` (Scheduling Engine)
- `rich>=13.0` (Interactive CLI)
- `questionary>=2.0` (Interactive CLI)
- `requests>=2.31.0` (Plugins)
- `beautifulsoup4>=4.12.0` (Plugins)
- `dnspython>=2.6.0` (Plugins)
- `python-nmap>=0.7.1` (Plugins)
- `openai>=1.14.0` (LLM Analysis)

## 2. Unused / Duplicate Dependencies
The following dependencies were identified across various legacy requirements files in the `archive/` folder but are no longer necessary for the core spine:
- `pandas` (Previously used for CSV generation, replaced by standard `csv` lib)
- `colorama` (Replaced entirely by `rich`)
- `typer` (Replaced by `argparse` + `rich` for dynamic menus)
- `Flask` (From old legacy repos, replaced by `FastAPI`)
- `psycopg2` (We standardized on `SQLite` to avoid heavy DB requirements)
- `celery` (Replaced by `asyncio` and `APScheduler`)

## 3. Recommended Removals
If you are running in an existing virtual environment, we recommend purging the following to prevent version conflicts:
```bash
pip uninstall -y pandas colorama typer flask psycopg2 celery
```

## 4. Version Conflicts
No active version conflicts were detected in the primary `requirements.txt`. 
The introduction of `SQLAlchemy 2.0+` requires strict ORM usage, which has been verified in `core/models.py`.
