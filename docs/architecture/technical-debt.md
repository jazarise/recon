# Technical Debt Register

As of the v1.0.0 release, the following technical debt items have been identified and categorized for resolution in v1.x or v2.0.

## Critical
- *None currently identified.*

## High
- **Plugin Sandboxing**: Currently relies on basic subprocess execution without strict OS-level containerization for individual plugins. A compromised binary could read local files accessible to the `reconx` user.
- **Workflow State Resilience**: Workflow execution state is held partially in memory during processing. If the API container crashes, running workflows are not automatically resumed or cleanly failed in the database.

## Medium
- **Database Connection Pooling**: While `asyncpg` is used, high concurrency workflow executions might exhaust the default SQLAlchemy connection pool size.
- **Asset Graph Queries**: Deduplication relies on basic indexing. As the dataset approaches 1M+ assets, recursive relationship lookups (e.g., Domain -> IP -> Port -> Vulnerability) will suffer performance degradation.
- **Reporting CPU Usage**: PDF generation blocks the asyncio event loop slightly despite threadpool offloading.

## Low
- **Deprecated Modules**: Old mock data generation scripts in `tests/fixtures/` should be cleaned up.
- **Temporary Implementations**: The local event bus used by the Workflow Engine needs to be replaced with Redis/RabbitMQ.
