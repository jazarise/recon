# Workflow Security Review

Workflows are dynamically interpreted YAML files defining sequences of operational reconnaissance execution.

## Findings
- Initial parsing utilized `yaml.load()`, rendering the orchestration layer vulnerable to malicious arbitrary Python object deserialization if an attacker fed a malicious `.yaml` file into the engine.

## Resolution
- Validated that `yaml.safe_load()` correctly interprets the rigid `Workflow` schema.
- The workflow execution schema inherently sandboxes execution strictly to registered plugins indexed within `reconx.core.plugin_manager`. Unrecognized command sequences abort workflow execution rather than attempting to execute them as generic bash commands.
