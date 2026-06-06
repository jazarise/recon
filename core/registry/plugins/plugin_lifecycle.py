from .plugin_schema import Plugin, PluginLifecycle

class PluginLifecycleManager:
    """Handles state transitions for plugins based on health and validation checks."""

    @staticmethod
    def mark_broken(plugin: Plugin, reason: str):
        plugin.status = PluginLifecycle.BROKEN
        # In a real system, we'd log the reason to the DB or analytics
        print(f"[-] Plugin {plugin.name} marked as BROKEN: {reason}")

    @staticmethod
    def mark_active(plugin: Plugin):
        plugin.status = PluginLifecycle.ACTIVE
        print(f"[+] Plugin {plugin.name} is ACTIVE.")

    @staticmethod
    def evaluate_status(plugin: Plugin, health_check_passed: bool, validation_passed: bool):
        if not validation_passed or not health_check_passed:
            PluginLifecycleManager.mark_broken(plugin, "Validation or health check failed.")
        elif plugin.status == PluginLifecycle.TESTING and health_check_passed and validation_passed:
            PluginLifecycleManager.mark_active(plugin)
