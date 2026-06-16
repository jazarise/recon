import importlib
import pkgutil
import sys
import os

class AdapterRegistry:
    def __init__(self):
        self._adapters = {}

    def register(self, capability: str, name: str, adapter_class):
        if capability not in self._adapters:
            self._adapters[capability] = {}
        self._adapters[capability][name] = adapter_class

    def get_adapters_for_capability(self, capability: str):
        return self._adapters.get(capability, {})

    def get_all_adapters(self):
        all_adapters = {}
        for cap, adapters in self._adapters.items():
            all_adapters.update(adapters)
        return all_adapters

adapter_registry = AdapterRegistry()

def load_adapters():
    """Dynamically load all adapters from modules.adapters"""
    # We will use importlib to dynamically load modules from 'modules.adapters'
    try:
        import modules.adapters
        for _, module_name, _ in pkgutil.iter_modules(modules.adapters.__path__):
            importlib.import_module(f"modules.adapters.{module_name}")
    except ImportError as e:
        print(f"Warning: Could not load adapters: {e}")

