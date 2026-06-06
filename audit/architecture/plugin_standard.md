# Unified Plugin Interface Standard

## The Problem
Historically, embedded repositories utilized wildly different execution entry points (`run()`, `launch()`, `execute()`, `scan()`), creating an unmaintainable web of wrappers.

## The Standard
All ReconX plugins **must** inherit from `PluginInterface` and implement the `execute(self, target, context)` method. 

### Mandatory Interface
```python
from core.plugin_manager.interface import PluginInterface

class ReconXPlugin(PluginInterface):
    name = "plugin_name"
    version = "1.0.0"

    def execute(self, target: str, context: dict) -> dict:
        # 1. Execute tool or API
        # 2. Parse raw output
        # 3. Return structured dictionary
        return {"status": "success", "findings": []}
        
    def normalize(self, results: dict) -> list:
        # Convert dictionary to core.models Objects
        pass
```

### Loading Mechanism
Plugins are automatically discovered and loaded dynamically by `core.plugin_manager.PluginManager`. **No repository-specific runner scripts (e.g., `metatron_launcher.py`) are allowed.**
