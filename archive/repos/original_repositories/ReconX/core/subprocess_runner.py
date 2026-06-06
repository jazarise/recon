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
from pathlib import Path

# Detect project root (this file is in core/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Ensure project root is in sys.path for core.* imports in plugins
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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
        adapter_file = PROJECT_ROOT / plugin_path / "adapter.py"
        if not adapter_file.exists():
            raise FileNotFoundError(f"Adapter not found at {adapter_file}")

        spec = importlib.util.spec_from_file_location("reconx_plugin", str(adapter_file))
        if not spec or not spec.loader:
            raise ImportError("Could not load spec for adapter")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "ToolAdapter"):
            raise AttributeError("Adapter module missing ToolAdapter class")

        adapter = module.ToolAdapter()
        
        # Execute the adapter logic
        if inspect.iscoroutinefunction(adapter.execute):
            result = await adapter.execute(config, context)
        else:
            result = adapter.execute(config, context)

        # Write result to STDOUT
        print(json.dumps({"status": "success", "data": result}))
        sys.exit(0)

    except Exception as e:
        # Write error to STDOUT in structured format
        print(json.dumps({"status": "error", "error": str(e), "type": type(e).__name__}))
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
