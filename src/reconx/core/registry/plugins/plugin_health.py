from .plugin_schema import Plugin
from .plugin_registry import plugin_registry_system

class PluginHealthCheck:
    """Invokes health checks on plugins."""

    @staticmethod
    def run_all_checks() -> dict:
        results = {}
        for name, plugin in plugin_registry_system.plugins.items():
            adapter_cls = plugin_registry_system.get_adapter_class(name)
            if not adapter_cls:
                results[name] = {"status": "unloaded"}
                continue
                
            try:
                adapter_instance = adapter_cls()
                health_data = adapter_instance.health()
                results[name] = health_data
            except Exception as e:
                results[name] = {"status": "error", "message": str(e)}
        return results
