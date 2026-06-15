from core.plugin_manager.interface import ReconXPlugin
class ToolAdapter(ReconXPlugin):
    def validate(self, options):
        pass

    def prepare(self, target, options):
        pass

    def execute(self, target, options):
        pass

    def normalize(self, raw_output):
        pass

    def cleanup(self):
        pass

# Auto-injected Metadata
PLUGIN_NAME = "wordlist"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for wordlist"

from core.plugin_base import standardize_output
import inspect
import sys

@standardize_output
async def run(target: str, context: dict) -> dict:
    mod = sys.modules[__name__]
    for name, obj in inspect.getmembers(mod, inspect.isclass):
        if hasattr(obj, 'execute') and obj.__module__ == __name__:
            instance = obj()
            if hasattr(instance, 'prepare'): instance.prepare(target, context)
            raw = instance.execute(target, context) if hasattr(instance, 'execute') else {}
            norm = instance.normalize(raw) if hasattr(instance, 'normalize') else raw
            if hasattr(instance, 'cleanup'): instance.cleanup()
            return {"success": True, "data": norm}
    return {"success": True, "data": "No executable class found"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = []
