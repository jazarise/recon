# Architecture Overview
ReconX utilizes a micro-engine architecture. The API routes dispatch execution requests to the `TaskQueue`. The `Scheduler` delegates atomic jobs derived from `Workflows` to the `EventBus`, which executes `Plugins`.
