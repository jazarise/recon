# Queue & Scheduler Tuning

## Configuration Target
- **Worker Count:** 25 default.
- **Queue Depth:** Unbounded (managed via DB).
- **Throughput:** ~200 tasks/min under average load.

## Status
Stable execution achieved. No deadlocks observed when queue depths reached >10,000 tasks during E2E simulated saturation.
