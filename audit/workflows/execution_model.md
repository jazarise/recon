# Execution Model

Before:
User -> CLI -> Plugin script -> JSON

After:
1. User requests a workflow via API or CLI.
2. `WorkflowEngine` loads YAML and builds execution graph.
3. `Orchestrator` creates a `WorkflowContext`.
4. `TaskQueue` manages state tracking.
5. Plugins fire asynchronously.
6. Plugins yield `Finding` objects to `WorkflowContext`.
7. `EventBus` signals the Dashboard and Database of new findings.
