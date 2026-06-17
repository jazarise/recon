# Plugin Development Guide

ReconX is highly extensible. You can write plugins to wrap any custom or third-party offensive security tool.

## Creating Your First Plugin
To create a plugin, inherit from the `ReconXPlugin` SDK class.

Here is an example of a simple `Echo` plugin:

```python
from sdk.plugin_sdk import ReconXPlugin, run_command, validate_target

class EchoPlugin(ReconXPlugin):
    @property
    def name(self) -> str:
        return "echo_test"
        
    @property
    def version(self) -> str:
        return "1.0.0"

    async def execute(self, target: str, **kwargs) -> str:
        if not validate_target(target):
            raise ValueError("Invalid target")
        # Securely execute the command (no shell=True)
        return await run_command(["echo", target])

    def parse(self, output: str) -> list:
        # Translate the output into the ReconX Schema
        return [
            {
                "type": "asset",
                "value": output.strip(),
                "asset_type": "domain"
            }
        ]
```

## Integrating into ReconX
Place your plugin folder inside `src/reconx/plugins/`. The `PluginManager` automatically discovers all Python packages in that directory that expose a `Plugin` class.
