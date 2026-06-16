# Module Ownership Matrix

This matrix defines the clear boundary and operational ownership of all top-level modules within the `reconx` package. 
There is no shared ownership.

| Module        | Owner / Scope | Responsibilities |
| ------------- | ------------- | ---------------- |
| `api`         | API | REST endpoints, WebSocket hubs, HTTP routing schemas. |
| `cli`         | CLI | Typer command-line interface, argument parsing, visual printing (Rich). |
| `core`        | Core Engine | Execution Orchestrator, TaskQueue, Scheduler, EventBus, WorkflowEngine. |
| `database`    | Database | SQLAlchemy schemas, alembic migrations, ORM sessions. |
| `plugins`     | Plugins | Concrete implementations of tools (web scanners, OSINT, reporting) that hook into the PluginManager. |
| `workflows`   | Workflows | YAML declarative graphs detailing execution sequences. |
| `dashboard`   | Frontend | The React/UI web console assets. |
| `modules`     | Extensibility | Specialized shared business logic components. |
| `agents`      | Autonomy | High-level decision making agents (actively refactoring). |
| `rules`       | Signatures | YAML-based signatures for vulnerability and intelligence hunting. |
| `prompts`     | LLM Config | Standardized AI/LLM instruction sets. |
