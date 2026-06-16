# ADR-004: Centralized Task Scheduler

## Context
ReconX delegates background scanning tasks (like port scanning or scraping) to background workers. The audit revealed the existence of three separate scheduling abstractions: `Scheduler`, `JobScheduler`, and `AsmScheduler`, creating parallel, disconnected execution flows that were difficult to monitor globally.

## Decision
All background operations will funnel through a single queue and execution broker:
- **Scheduler:** `reconx.core.scheduler.Scheduler`
- **Queue:** `reconx.core.queue.TaskQueue`

The `JobScheduler` and `AsmScheduler` (Attack Surface Management scheduler) have been deprecated and archived. Their unique scheduling profiles will be adapted into standard plugins that submit standard tasks to the unified `TaskQueue`.

## Consequences
- **Positive:** Standardizes worker execution. The dashboard and API only need to query a single TaskQueue to determine system load.
- **Negative:** ASM logic must be slightly rewritten to interface with the generic queue rather than its custom scheduling wrapper.

## Alternatives Considered
- Maintaining dedicated queues for different types of operations (e.g. an "ASM Queue" vs a "Job Queue"). Rejected because the added complexity of managing multiple concurrent thread pools outweighs the organizational benefit for a streamlined scanning engine.
