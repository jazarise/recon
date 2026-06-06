# Architecture Consolidation Plan

## Step 1 — Identify Architectural Duplicates
Based on the Stage 0 inventory, the following classifications have been finalized:

### Keep
- `core/` - Single orchestrator and execution engine
- `modules/` - Categorized core functionality
- `plugins/` - Standardized tool integrations
- `workflows/` - YAML execution definitions
- `api/` - FastAPI gateway
- `dashboard/` - React frontend
- `reports/` - Unified output artifacts
- `tests/` - System and unit tests

### Merge / Already Archived
- `repositories/` -> moved to `archive/repos/`
- `original_repositories/` -> moved to `archive/repos/`
- `legacy_modules/`, `old_cli/`, `experimental/`, `prototype/`, `backup/`, `deprecated/` -> moved to `archive/deprecated/`

## Consolidation Actions
1. **Single Entry Point**: Established `reconx.py` as the exclusive CLI. All other launchers have been archived.
2. **Unified Core Engine**: Deprecated legacy executor scripts in favor of `core/orchestrator.py`.
3. **Standardized Interfaces**: Forced all plugins to use `core/plugin_manager/interface.py`.
4. **Data Unification**: Mandated that all findings use the `core/models.py` definitions (Asset, Vulnerability, Service).
5. **Workflow Standard**: Chose YAML inside `workflows/` as the single source of truth for execution.
6. **Reporting & UI**: Reports are strictly generated from Findings via the `api/` endpoints. No direct plugin-to-UI communication is permitted.
