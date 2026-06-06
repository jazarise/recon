import importlib
from typing import Any, Optional

class PluginLoader:
    """Dynamically loads plugin entry points."""

    @staticmethod
    def load_adapter_class(entrypoint: str) -> Optional[Any]:
        """
        Dynamically imports the adapter class specified in the entrypoint.
        Example entrypoint: 'modules.adapters.subfinder_adapter.SubfinderAdapter'
        """
        try:
            module_path, class_name = entrypoint.rsplit(".", 1)
            module = importlib.import_module(module_path)
            adapter_class = getattr(module, class_name)
            return adapter_class
        except (ValueError, ImportError, AttributeError) as e:
            print(f"[-] Failed to load entrypoint {entrypoint}: {e}")
            return None
