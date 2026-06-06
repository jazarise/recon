# Orchestration Design

The central `Orchestrator` (`core/orchestrator.py`) handles async parallel execution.

- **Dynamism**: Plugins are loaded dynamically from the `modules/` directory at runtime.
- **Asynchrony**: Uses `asyncio.create_task()` to run plugins in parallel. Plugins that block natively are run via `asyncio.to_thread()`.
- **Event Bus**: The Orchestrator emits real-time events (`PluginStarted`, `FindingCreated`, `WorkflowCompleted`) allowing external components like Dashboards to update immediately.
