# Final ReconX Architecture

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
