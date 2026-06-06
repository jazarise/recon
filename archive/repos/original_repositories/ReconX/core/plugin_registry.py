import json
from pathlib import Path
from typing import Dict, Any

class PluginRegistry:
    def __init__(self, registry_file: str = "e:/ReconX/intelligence/plugin_registry.json"):
        self.registry_file = Path(registry_file)
        self.plugins: Dict[str, Any] = {}
        self.load_registry()

    def load_registry(self) -> None:
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                data = json.load(f)
                self.plugins = data.get("plugins", {})

    def register_plugin(self, name: str, path: str) -> None:
        self.plugins[name] = {"path": path}
        self.save_registry()

    def save_registry(self) -> None:
        with open(self.registry_file, 'w') as f:
            json.dump({"plugins": self.plugins}, f, indent=4)

    def get_plugin(self, name: str) -> Dict[str, Any]:
        return self.plugins.get(name, {})
