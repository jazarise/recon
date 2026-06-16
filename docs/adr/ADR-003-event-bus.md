# ADR-003: Unified Event Bus

## Context
ReconX components (Orchestrator, Plugins, API) communicate asynchronously using event signals. However, duplicate `EventBus` implementations existed: one primarily in `reconx.core.event_bus` and a shadowed nested instance inside `reconx.core.reconx.core.events`. This caused fragmented signaling where API events were entirely disconnected from Orchestrator events.

## Decision
There will be **One EventBus** implementation (`reconx.core.event_bus.EventBus`). All modules broadcasting or subscribing to signals must import and interact with this singular module. 

## Consequences
- **Positive:** Guarantees signal delivery across the entire application domain. Simplifies debugging event traces.
- **Negative:** Requires strict typed event payloads (One Event Model) to ensure cross-module compatibility.

## Alternatives Considered
- Running a distributed bus like Redis natively for internal module signaling. Rejected because it violates the zero-config initial install requirement for standard deployments. The in-memory Python `EventBus` is sufficient for localized execution.
