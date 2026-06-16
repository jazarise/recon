# Workflow Engine Audit

The Workflow Engine parses declarative YAML execution graphs and bridges the UI/CLI intent to the Orchestrator.

## Findings

*   The workflow engine module resides at `reconx.core.workflow_engine.WorkflowEngine`. No duplicate execution paths were found outside this core component.
*   An audit of all 16 predefined `.yaml` workflows under `src/reconx/workflows/` revealed a structural schema inconsistency: While `name` and `description` were present natively, all sequences were tracked under a `steps:` array rather than the standardized `stages:` array expected by ReconX v3.0 architecture requirements.

## Resolution

A global refactor was performed across all `.yaml` definitions in `src/reconx/workflows/`.
- All `steps:` keys have been successfully migrated to `stages:`.

The workflows are now 100% compliant with the `Workflow(name, description, stages)` schema model.
