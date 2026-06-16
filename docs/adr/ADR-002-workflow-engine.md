# ADR-002: Workflow Engine Schema Enforcement

## Context
ReconX utilizes declarative YAML files to define execution pipelines (e.g. `deep_scan.yaml`). During Stage 2, it was discovered that these files were lacking structural consistency; workflows arbitrarily used `steps` or `stages` as the sequence array identifier.

## Decision
All `.yaml` workflow graphs must strictly implement the standard schema:
```yaml
name: [Workflow Name]
description: [Description]
stages:
  - id: [step id]
    plugin: [plugin target]
```
The `WorkflowEngine` will reject any `.yaml` configuration that fails to supply `name`, `description`, and `stages` keys.

## Consequences
- **Positive:** UI/CLI representations are uniform. The Orchestrator engine logic can confidently iterate the `stages` key without probing `steps` or nested lists.
- **Negative:** Backwards compatibility with deprecated user workflows using `steps` is broken.

## Alternatives Considered
- Support dual-parsing of `steps` and `stages`. Rejected because ReconX v3.0 emphasizes explicit clarity and minimal duplicated logic paths.
