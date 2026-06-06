# Workflow Specification

All workflows in ReconX are defined in YAML format and stored in the `workflows/` directory.

## Structure
- `name`: Unique identifier for the workflow.
- `steps`: List of plugins to execute. Supports dependency mapping.

Example:
```yaml
name: web_assessment
steps:
  - httpx
  - nuclei:
      depends_on:
        - httpx
```
