from fastapi import APIRouter
from core.registry.plugins import plugin_registry_system
from core.registry.plugins.plugin_health import PluginHealthCheck

router = APIRouter(prefix="/api/plugins", tags=["Plugin Management"])

@router.get("/")
def list_plugins():
    return {name: p.dict() for name, p in plugin_registry_system.plugins.items()}

@router.get("/health")
def health_check():
    return PluginHealthCheck.run_all_checks()

@router.post("/reload")
def reload_registry():
    plugin_registry_system.plugins.clear()
    plugin_registry_system.adapter_classes.clear()
    plugin_registry_system.load_registry()
    return {"status": "success", "plugins_loaded": len(plugin_registry_system.plugins)}
