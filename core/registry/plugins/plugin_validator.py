from .plugin_schema import Plugin
from .plugin_dependency_manager import PluginDependencyManager
from .plugin_lifecycle import PluginLifecycleManager

class PluginValidator:
    """Validates plugins on startup ensuring contract compliance and dependencies."""

    @staticmethod
    def validate(plugin: Plugin) -> bool:
        """Runs all checks to ensure plugin can safely transition to ACTIVE."""
        
        # 1. Check dependencies
        if not PluginDependencyManager.check_dependencies(plugin.dependencies):
            print(f"[-] Validation failed for {plugin.name}: missing dependencies {plugin.dependencies}")
            PluginLifecycleManager.mark_broken(plugin, "Missing dependencies")
            return False

        # 2. Check capability assignment
        if not plugin.capability.startswith(("discovery.", "vuln.", "content.", "osint.")):
            PluginLifecycleManager.mark_broken(plugin, f"Invalid capability string: {plugin.capability}")
            return False
            
        return True
