# Workflow Security

## YAML Parsing
ReconX strictly uses `yaml.safe_load` to parse incoming workflows. This mitigates risks associated with Python object instantiation vulnerabilities via standard `yaml.load`.

## Graph Validation
Before any workflow is executed, it is converted into a `DependencyGraph`. The engine validates the graph to ensure there are no cyclical dependencies (e.g., Task A depends on Task B, which depends on Task A). If a cycle is detected, the workflow is rejected with a 400 Bad Request to prevent infinite hanging executions.
