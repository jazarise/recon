# ReconX Architecture Audit

## Directory Tree
```text
├── ai/
├── api/
├── audit/
├── cli/
├── config/
├── core/
├── dashboard/
├── docs/
├── events/
├── installers/
├── integrations/
├── intelligence/
├── logs/
├── modules/
├── outputs/
├── plugins/
├── projects/
├── reports/
├── repository_audit/
├── results/
├── scripts/
├── setup/
├── tests/
├── tools/
├── workflows/
```

## Core Components
- **Plugin System**: `core/plugin_loader.py` manages loading dynamic plugins.
- **Workflow Engine**: `core/workflow_engine.py` orchestrates tasks.
- **Database Layer**: `core/database.py` and `core/result_store.py`.
- **CLI Layer**: `reconx.py` serves as the primary entry point.
- **AI Layer**: Plugins under `plugins/recon/llm_analysis`.

## Highlights & Issues
- **Missing Modules**: SQLAlchemy dependencies and missing subprocess binaries.
- **Dead Components**: Many plugins are wrappers without the underlying binary.
