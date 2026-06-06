# Architecture Principles

These rules are non-negotiable and enforce the integrity of ReconX:

### Rule 1: The Unified Data Layer
All plugins, modules, and internal functions MUST return `Finding` objects as defined in `core/models/finding.py`. Custom JSON dictionaries or flat text outputs are strictly prohibited.

### Rule 2: Single Source of Truth
No plugin-specific databases or localized JSON tracking files. All state and findings are strictly managed by the centralized SQLAlchemy ORM.

### Rule 3: Orchestrator Supremacy
Plugins cannot call other plugins or spawn independent background threads. The `Workflow Engine` and `Orchestrator` exclusively control all execution and concurrency.

### Rule 4: No Duplicate Capabilities
If a feature exists (e.g. port scanning via Nmap), a new plugin duplicating this exact feature (e.g. Masscan) will only be accepted if it demonstrates a significant (10x) performance improvement or covers a fundamentally different use case.
