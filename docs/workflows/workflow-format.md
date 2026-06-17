# Workflow Format

Workflows in ReconX define the specific sequence of plugins to execute against a target. They are written in YAML.

## Schema

```yaml
name: string        # Unique name of the workflow
description: string # Human-readable description

tasks:
  - id: string      # Unique ID for this task
    plugin: 
      name: string  # Name of the plugin to run
    depends_on:     # (Optional) List of Task IDs that must complete first
      - string
```

The engine reads this schema and constructs a Directed Acyclic Graph (DAG) for execution.
