# ReconX Architecture

## Core Components
1. **Interactive CLI (`reconx.py`)**: Entry point for Operators.
2. **Orchestrator**: Manages the execution lifecycle.
3. **Workflow Engine**: Parses YAML and builds a DAG (Directed Acyclic Graph).
4. **Execution Manager**: Handles async/subprocess tool execution with strict timeouts.
5. **Correlation Engine**: Post-processes raw JSON output to build an Asset Graph (Domain -> IP -> Services).
6. **Asset Database**: SQLite-based persistent storage via SQLAlchemy.
7. **Event Bus**: Pub/sub system bridging the Orchestrator with the Live React Dashboard.
