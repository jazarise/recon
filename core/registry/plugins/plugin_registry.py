import os
import json
from typing import Dict, List
from .plugin_schema import Plugin, PluginLifecycle
from .plugin_loader import PluginLoader

class PluginRegistrySystem:
    """Singleton registry holding verified and parsed plugins."""

    def __init__(self, registry_file: str = "plugins/registry.json"):
        self.registry_file = registry_file
        self.plugins: Dict[str, Plugin] = {}
        self.adapter_classes: Dict[str, Any] = {}

    def load_registry(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        path = os.path.join(base_dir, self.registry_file)
        
        if not os.path.exists(path):
            print(f"[-] Registry file not found at {path}")
            return

        with open(path, "r") as f:
            data = json.load(f)
            
        for name, meta in data.items():
            meta["name"] = name
            try:
                plugin = Plugin(**meta)
                self.plugins[name] = plugin
                
                # Attempt to load adapter
                if plugin.status in [PluginLifecycle.ACTIVE, PluginLifecycle.TESTING]:
                    adapter_cls = PluginLoader.load_adapter_class(plugin.entrypoint)
                    if adapter_cls:
                        self.adapter_classes[name] = adapter_cls
                    else:
                        plugin.status = PluginLifecycle.BROKEN
            except Exception as e:
                print(f"[-] Invalid plugin schema for {name}: {e}")

    def get_plugins_for_capability(self, capability: str) -> List[Plugin]:
        return [p for p in self.plugins.values() if p.capability == capability and p.status == PluginLifecycle.ACTIVE]

    def get_adapter_class(self, plugin_name: str):
        return self.adapter_classes.get(plugin_name)

plugin_registry_system = PluginRegistrySystem()
