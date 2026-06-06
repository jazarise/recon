# ReconX Repository Structure
*Generated during Documentation Remediation*

This document reflects the exact, verified structure of the ReconX repository post-archive cleanup.

## Core Production Directories

| Directory | Purpose | Status |
|-----------|---------|--------|
| `api/` | FastAPI gateway and websocket routes. | `VERIFIED` |
| `archive/` | Safe storage for experimental AI concepts and legacy code. | `VERIFIED` |
| `audit/` | Storage for automated validation reports. | `VERIFIED` |
| `core/` | Engine logic (Orchestrator, ExecutionManager, WorkflowEngine). | `VERIFIED` |
| `dashboard/` | React/Vite frontend. | `VERIFIED` |
| `docs/` | Comprehensive markdown documentation suite. | `VERIFIED` |
| `logs/` | Structured JSON log outputs. | `VERIFIED` |
| `outputs/` | JSON and HTML report generation folder. | `VERIFIED` |
| `plugins/` | Dynamic reconnaissance modules (`adapter.py`). | `VERIFIED` |
| `scripts/` | Shell scripts like `verify_environment.sh` and `install.sh`. | `VERIFIED` |
| `tests/` | Unit and integration tests (Pytest). | `VERIFIED` |
| `workflows/` | YAML workflow templates (`basic.yaml`, `medium.yaml`). | `VERIFIED` |

All other arbitrary folders have been safely archived into `<RECONX_ROOT>/archive/` to ensure a pristine, production-ready environment.
