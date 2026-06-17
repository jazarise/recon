from typing import Dict, Type, List
from reconx.core.plugins.base import ReconXPlugin, PluginResult
from reconx.core.plugins.registry import PluginRegistry
from reconx.core.plugins.loader import PluginLoader
from reconx.core.plugins.executor import PluginExecutor
from reconx.core.plugins.sandbox import PluginSandbox
from reconx.core.plugins.exceptions import PluginError
from sqlalchemy.ext.asyncio import AsyncSession
import yaml


class PluginManager:
    def __init__(self, plugin_dir: str = "src/reconx/plugins"):
        self.registry = PluginRegistry(plugin_dir)
        self.plugins: Dict[str, Type[ReconXPlugin]] = {}
        self.metadata: Dict[str, dict] = {}

    def list_plugins(self) -> List[dict]:
        return list(self.metadata.values())

    def load_plugin(self, name: str) -> None:
        # Find the plugin dir
        plugin_paths = self.registry.discover_plugins()
        target_path = None
        for p in plugin_paths:
            try:
                with open(p, "r", encoding="utf-8") as f:
                    meta = yaml.safe_load(f)
                    if meta.get("name") == name:
                        target_path = p.parent
                        self.metadata[name] = meta
                        break
            except Exception:
                continue  # nosec B112

        if not target_path:
            raise PluginError(f"Plugin {name} not found")

        plugin_class = PluginLoader.load_plugin(target_path)
        self.plugins[name] = plugin_class

    def unload_plugin(self, name: str):
        if name in self.plugins:
            del self.plugins[name]

    def reload_plugin(self, name: str):
        self.unload_plugin(name)
        self.load_plugin(name)

    def load_all(self):
        paths = self.registry.discover_plugins()
        for p in paths:
            try:
                with open(p, "r", encoding="utf-8") as f:
                    meta = yaml.safe_load(f)
                    name = meta.get("name")
                    if name:
                        self.load_plugin(name)
            except Exception:
                pass  # nosec B110

    async def execute_plugin(
        self, db: AsyncSession, name: str, target_id: str, target_val: str
    ) -> PluginResult:
        if name not in self.plugins:
            self.load_plugin(name)

        plugin_class = self.plugins[name]
        plugin_instance = plugin_class()

        # Populate instance metadata
        meta = self.metadata.get(name, {})
        plugin_instance.name = meta.get("name", "")
        plugin_instance.version = meta.get("version", "")

        sandbox = PluginSandbox(timeout=300)
        executor = PluginExecutor(db, sandbox)

        return await executor.run(plugin_instance, target_id, target_val)


plugin_manager = PluginManager()
