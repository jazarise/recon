# ReconX Plugin Guide

## Dynamic Auto-Registration
ReconX uses dynamic loading. To add a custom module, simply drop a folder into `plugins/` containing an `adapter.py` file.

### Example `plugins/my_custom_tool/adapter.py`
```python
from core.plugin_interface import PluginInterface

class ToolAdapter(PluginInterface):
    async def execute(self, config: dict, context: dict) -> dict:
        target = context.get("target")
        return {"status": "success", "data": f"Scanned {target}"}
```

The `PluginLoader` will automatically register `my_custom_tool` at runtime. No core code modification is required.
