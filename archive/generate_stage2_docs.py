import os
from pathlib import Path

base_dir = Path("e:/ReconX/Reconx_V_2.0.0")
arch_dir = base_dir / "audit" / "architecture"
arch_dir.mkdir(parents=True, exist_ok=True)

consolidation_plan = """# Architecture Consolidation Plan

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
"""

final_architecture = """# Final ReconX Architecture

## Target Structure
The repository has been successfully consolidated into the following definitive hierarchy:

```text
ReconX/
├── reconx.py                # Single Entry Point CLI
├── core/                    # Unified Core Engine
│   ├── orchestrator.py      # Main Execution Flow
│   ├── plugin_manager.py    # Standardized Loader
│   ├── workflow_engine.py   # YAML Pipeline Runner
│   ├── config.py            # Global Config
│   ├── database.py          # SQLAlchemy Session Manager
│   └── event_bus.py         # Async Event Emitter
├── modules/                 # Functional Domains (recon, osint, web, etc.)
├── plugins/                 # Standardized Tool Integrations
├── workflows/               # YAML Execution Plans
├── api/                     # Unified FastAPI Gateway
├── dashboard/               # Single React Dashboard UI
├── reports/                 # Centralized Report Engine
├── tests/                   # Pytest Suites
├── docs/                    # Official Documentation
├── tools/                   # Developer Tools (build/ etc.)
└── archive/                 # Repositories, Deprecated Code, and Generated Assets
```

Any directories or systems attempting to operate outside of this hierarchy are strictly forbidden. The system now guarantees **one execution path, one data model, and one UI.**
"""

plugin_standard = """# Unified Plugin Interface Standard

## The Problem
Historically, embedded repositories utilized wildly different execution entry points (`run()`, `launch()`, `execute()`, `scan()`), creating an unmaintainable web of wrappers.

## The Standard
All ReconX plugins **must** inherit from `PluginInterface` and implement the `execute(self, target, context)` method. 

### Mandatory Interface
```python
from core.plugin_manager.interface import PluginInterface

class ReconXPlugin(PluginInterface):
    name = "plugin_name"
    version = "1.0.0"

    def execute(self, target: str, context: dict) -> dict:
        # 1. Execute tool or API
        # 2. Parse raw output
        # 3. Return structured dictionary
        return {"status": "success", "findings": []}
        
    def normalize(self, results: dict) -> list:
        # Convert dictionary to core.models Objects
        pass
```

### Loading Mechanism
Plugins are automatically discovered and loaded dynamically by `core.plugin_manager.PluginManager`. **No repository-specific runner scripts (e.g., `metatron_launcher.py`) are allowed.**
"""

workflow_standard = """# Unified Workflow System Standard

## Consolidation
Previous iterations of ReconX relied on a mix of python scripts, shell scripts, and custom pipeline formats to run tools.

## The New Standard
We have standardized exclusively on **YAML Workflows** managed by `core.workflow_engine.WorkflowEngine`.

### Structure
Workflows live in the `workflows/` directory.

### Example Schema
```yaml
name: enterprise_recon
description: "Full spectrum discovery and vulnerability mapping"

steps:
  - id: step1_discovery
    plugin: subfinder
    config:
      timeout: 300
      
  - id: step2_resolution
    plugin: dnsx
    depends_on: [step1_discovery]
    
  - id: step3_scanning
    plugin: nuclei
    depends_on: [step2_resolution]
```

### Execution Flow
1. **Target** is provided via CLI (`reconx.py`).
2. **Workflow Engine** parses the YAML.
3. **Execution Manager** invokes the corresponding standardized **Plugins**.
4. Plugins return data that goes strictly to the unified **Findings**.
"""

data_model = """# Unified Data Model

## Finding Normalization
To prevent chaos, ReconX no longer permits tools to output arbitrary JSON/TXT formats directly to reports or the dashboard. All data must flow through the SQLAlchemy Data Models defined in `core/models.py`.

### Core Entities
Every piece of output must be mapped to one of the following structured objects:

1. **Asset**: `type` (domain, ip, asn, url), `value`, `first_seen`, `tags`
2. **Service**: `port`, `protocol`, `service_name`, `product`, `version`
3. **Vulnerability**: `name`, `severity`, `description`, `discovered_at`
4. **ScanHistory**: Tracks workflow executions and their completion status.

### Flow
`Tool Output -> Plugin Normalize() -> SQLAlchemy Object -> SQLite Database -> API -> Dashboard / Reports`

No plugin is permitted to bypass the SQLite database or generate an ad-hoc HTML report. The centralized Reporting module consumes `Finding` objects and emits the standardized JSON, HTML, PDF, or Markdown formats.
"""

files = {
    "consolidation_plan.md": consolidation_plan,
    "final_architecture.md": final_architecture,
    "plugin_standard.md": plugin_standard,
    "workflow_standard.md": workflow_standard,
    "data_model.md": data_model
}

for filename, content in files.items():
    with open(arch_dir / filename, "w", encoding="utf-8") as f:
        f.write(content)

print("[+] Successfully generated all Stage 2 architecture deliverables.")
