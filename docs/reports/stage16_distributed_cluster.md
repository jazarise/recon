# Stage 16: Distributed Cluster Architecture

## Master-Worker Topology
The framework successfully decoupled into a `MasterNode` managing the stateful `JobQueue` and stateless `WorkerNode`s. Heavy workloads (e.g., executing multiple plugins across massive target lists) are now seamlessly balanced across worker pools.

## Fault Tolerance
The simulated `MessageBroker` implements robust fault tolerance. If a worker process fails unexpectedly, it emits `TASK_FAILED`, triggering the Master to instantly re-queue the task with elevated priority, ensuring zero data loss during wide campaigns.

## Global Attack Surface Map
Instead of localized targets, the `CentralAggregator` intercepts findings from all workers and binds them into a `Global Attack Surface Graph`. This allows the detection of cross-domain shared infrastructure (e.g., two distinct target domains pointing to the same backend AWS node).
