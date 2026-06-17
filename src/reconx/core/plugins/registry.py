from pathlib import Path
from typing import List


class PluginRegistry:
    def __init__(self, plugin_dir: str = "src/reconx/plugins"):
        self.plugin_dir = Path(plugin_dir)

    def discover_plugins(self) -> List[Path]:
        return list(self.plugin_dir.rglob("plugin.yaml"))
