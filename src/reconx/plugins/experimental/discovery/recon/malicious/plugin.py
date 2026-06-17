from reconx.core.plugin_base import standardize_output
import time


class Plugin:
    name = 'malicious'
    category = 'recon'
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        mode = config.get("mode", "crash")
        
        if mode == "crash":
            raise MemoryError("Simulated memory corruption or segfault")
            
        if mode == "infinite_loop":
            # Simulate a blocking C-extension or unyielding while loop
            # This should trigger the ExecutionManager hard timeout
            while True:
                time.sleep(1)
                
        return {"plugin": "malicious", "status": "survived"}

# Auto-injected Metadata
PLUGIN_NAME = "malicious"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for malicious"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = []
