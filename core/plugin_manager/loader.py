"""
ReconX Plugin Loader — discovers and loads plugins from the plugins/ directory tree.
Supports both flat (plugins/<name>/adapter.py) and nested
(plugins/<category>/<name>/adapter.py) layouts.
"""
from core.paths import PLUGINS_DIR


import importlib.util
from pathlib import Path

from core.plugin_manager.interface import ReconXPlugin
from core.logging.logger import setup_logger

logger = setup_logger("PluginManager")


class PluginManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PluginManager, cls).__new__(cls)
            cls._instance.plugins = {}
            cls._instance.plugin_dir = PLUGINS_DIR
        return cls._instance

    @classmethod
    def load(cls, name: str):
        instance = cls()
        return instance.get_plugin(name)

    def __init__(self):
        pass

    def discover_and_load(self):
        """Recursively walk the plugins directory looking for adapter.py or plugin.py files."""
        self.plugins.clear()

        plugin_files = list(self.plugin_dir.rglob("adapter.py")) + list(self.plugin_dir.rglob("plugin.py"))
        for adapter_path in plugin_files:
            if "__pycache__" in str(adapter_path):
                continue
                
            item = adapter_path.parent
            plugin_name = item.name
            if plugin_name in self.plugins:
                # Resolve duplicates by allowing nested path overrides or logging collision
                logger.warning(f"Duplicate plugin name detected: {plugin_name} at {adapter_path}. Skipping.")
                continue
            self._load_plugin(plugin_name, adapter_path)

    def _load_plugin(self, name: str, adapter_path: Path):
        try:
            spec = importlib.util.spec_from_file_location(
                f"reconx_plugin_{name}", str(adapter_path)
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "ToolAdapter") and issubclass(module.ToolAdapter, ReconXPlugin):
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
