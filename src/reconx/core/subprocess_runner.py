"""
ReconX Subprocess Runner — isolated plugin execution sandbox.
Receives plugin path, config, and context via STDIN (JSON).
Returns structured result via STDOUT (JSON).
"""

import sys
import json
import asyncio
import inspect
import importlib.util

from reconx.core.paths import BASE_DIR

# Ensure project root is in sys.path for core.* imports in plugins
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

async def main():
    try:
        # Read payload from STDIN
        payload_raw = sys.stdin.read()
        if not payload_raw:
            raise ValueError("No payload provided on STDIN")
            
        payload = json.loads(payload_raw)
        plugin_path = payload.get("plugin_path")
        config = payload.get("config", {})
        context = payload.get("context", {})

        if not plugin_path:
            raise ValueError("plugin_path missing from payload")

        # Dynamically load the adapter
        adapter_file = BASE_DIR / plugin_path / "adapter.py"
        if not adapter_file.exists():
            adapter_file = BASE_DIR / plugin_path / "plugin.py"
        if not adapter_file.exists():
            raise FileNotFoundError(f"Adapter/Plugin not found at {adapter_file}")

        spec = importlib.util.spec_from_file_location("reconx_plugin", str(adapter_file))
        if not spec or not spec.loader:
            raise ImportError("Could not load spec for adapter")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        adapter = None
        if hasattr(module, "ToolAdapter"):
            adapter = module.ToolAdapter()
        elif hasattr(module, "Plugin"):
            adapter = module.Plugin()
        else:
            raise AttributeError("Adapter module missing ToolAdapter or Plugin class")
        
        # Execute the adapter logic
        if hasattr(adapter, "execute"):
            if inspect.iscoroutinefunction(adapter.execute):
                result = await adapter.execute(config, context)
            else:
                result = adapter.execute(config, context)
        elif hasattr(adapter, "run"):
            if inspect.iscoroutinefunction(adapter.run):
                result = await adapter.run(target=context.get("target"), context=context)
            else:
                result = adapter.run(target=context.get("target"), context=context)
        else:
            raise AttributeError("Adapter missing execute or run method")

        # Write result to STDOUT
        print(json.dumps({"status": "success", "data": result}))
        sys.exit(0)

    except Exception as e:
        # Write error to STDOUT in structured format
        print(json.dumps({"status": "error", "error": str(e), "type": type(e).__name__}))
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
