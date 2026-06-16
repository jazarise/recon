# Event System Audit

The Event System manages real-time messaging, signals, and asynchronous callbacks within the ReconX platform.

## Findings

The architecture inventory revealed two separate `EventBus` implementations inside the `core` package:
1. `reconx.core.event_bus.EventBus`
2. The nested duplicate in `reconx.core.reconx.core.events.EventBus`

## Resolution

The nested implementation was completely archived (along with the rest of the duplicated `core.reconx` package).

ReconX now strictly relies on the single primary implementation:
- **Event Bus:** `reconx.core.event_bus.EventBus`

All signals and notifications emitted by plugins, the orchestrator, or scheduled workers must pipe through this singular instance.
