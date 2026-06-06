"""
ReconX Plugin Loader — discovers and loads plugins from the plugins/ directory tree.
Supports both flat (plugins/<name>/adapter.py) and nested
(plugins/<category>/<name>/adapter.py) layouts.
"""

import importlib.util
from pathlib import Path
from core.paths import PLUGINS_DIR
from core.plugin_interface import PluginInterface
from core.logger import setup_logger

logger = setup_logger("PluginLoader")


class PluginLoader:
    def __init__(self):
        self.plugins: dict = {}
        self.plugin_dir = PLUGINS_DIR

    def discover_and_load(self):
        """Walk the plugins directory up to 2 levels deep looking for adapter.py files."""
        self.plugins.clear()

        # First-level: plugins/<name>/adapter.py
        # Second-level: plugins/<category>/<name>/adapter.py
        search_dirs = [self.plugin_dir]
        for item in self.plugin_dir.iterdir():
            if item.is_dir() and item.name not in ("__pycache__",):
                search_dirs.append(item)

        for search_dir in search_dirs:
            if not search_dir.is_dir():
                continue
            for item in search_dir.iterdir():
                if not item.is_dir() or item.name == "__pycache__":
                    continue
                adapter_path = item / "adapter.py"
                if not adapter_path.exists():
                    continue
                plugin_name = item.name
                if plugin_name in self.plugins:
                    # Already registered — don't overwrite (first discovery wins)
                    continue
                self._load_plugin(plugin_name, adapter_path)

    def _load_plugin(self, name: str, adapter_path: Path):
        try:
            spec = importlib.util.spec_from_file_location(
                f"reconx_plugin_{name}", str(adapter_path)
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "ToolAdapter") and issubclass(module.ToolAdapter, PluginInterface):
                self.plugins[name] = module.ToolAdapter()
                logger.debug(f"Registered plugin: {name}")
        except Exception as e:
            logger.error(f"Failed to load plugin {name}: {e}")

    def get_plugin(self, name: str):
        if not self.plugins:
            self.discover_and_load()
        return self.plugins.get(name)

    def list_plugins(self) -> list:
        if not self.plugins:
            self.discover_and_load()
        return list(self.plugins.keys())
