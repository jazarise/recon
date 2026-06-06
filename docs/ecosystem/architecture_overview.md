# Architecture Overview

ReconX is a pure Python async framework.
- **Workflow Engine:** Resolves dependencies via `graphlib.TopologicalSorter`.
- **Event Bus:** Async pub/sub for cross-module decoupling.
- **Data Layer:** Unified mapping to SQLite via SQLAlchemy.
