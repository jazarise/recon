import time
from typing import Dict, Any, List
from reconx.core.registry import capability_registry, SelectionStrategy
from reconx.core.models import AdapterResult
from reconx.core.correlation import CorrelationEngine
from reconx.core.registry.plugins import plugin_registry_system, PluginSandbox, PluginValidator
from reconx.core.registry.modules import get_native_module
from reconx.core.events.event_stream import event_stream

class CapabilityManager:
    def __init__(self):
        self.metrics = []
        self.correlation_engine = CorrelationEngine()
        
        # Load and validate plugins on startup
        plugin_registry_system.load_registry()
        for name, plugin in plugin_registry_system.plugins.items():
            PluginValidator.validate(plugin)

    def select_plugins(self, capability: str, strategy: SelectionStrategy) -> List[Any]:
        # Returns validated adapter instances mapped from registered plugins
        plugins = plugin_registry_system.get_plugins_for_capability(capability)
        selected_adapters = []
        for p in plugins:
            cls = plugin_registry_system.get_adapter_class(p.name)
            if cls:
                selected_adapters.append(cls())
        return selected_adapters

    def run(self, capability: str, target: str, strategy: SelectionStrategy = SelectionStrategy.ALL) -> Dict[str, Any]:
        """
        Executes a capability by resolving it to its underlying native module and plugins.
        """
        print(f"[*] Running capability: {capability} against {target}")
        start_time = time.time()
        
        cap = capability_registry.get_capability(capability)
        if not cap:
            return {"error": f"Capability {capability} not found"}

        final_result = AdapterResult()

        # 1. Execute Canonical Native Module (if it exists)
        native_module = get_native_module(capability)
        if native_module:
            print(f"[*] Executing Native Canonical Module for {capability}")
            try:
                native_res = native_module.execute(target)
                for asset in native_res.assets:
                    event_stream.sync_emit("node.added", {
                        "id": asset.id, 
                        "label": asset.value, 
                        "group": asset.type.name.lower(), 
                        "val": 4
                    })
                final_result.assets.extend(native_res.assets)
                final_result.findings.extend(native_res.findings)
                final_result.relationships.extend(native_res.relationships)
                final_result.evidence.extend(native_res.evidence)
            except Exception as e:
                print(f"[-] Native Module execution failed: {e}")

        # 2. Execute External Plugins
        selected_adapters = self.select_plugins(capability, strategy)
        for adapter in selected_adapters:
            print(f"[*] Executing Plugin Adapter: {adapter.__class__.__name__}")
            result = PluginSandbox.execute(adapter, target=target, timeout_seconds=30)
            
            for asset in result.assets:
                event_stream.sync_emit("node.added", {
                    "id": asset.id, 
                    "label": asset.value, 
                    "group": asset.type.name.lower(), 
                    "val": 4
                })

            final_result.assets.extend(result.assets)
            final_result.findings.extend(result.findings)
            final_result.relationships.extend(result.relationships)
            final_result.evidence.extend(result.evidence)

        # Correlate into Intelligence Graph
        intelligence_graph = self.correlation_engine.process(final_result)

        # Feed into Drift Detector for ASM capabilities
        from core.asm.drift_detector import drift_detector
        drift_detector.process_result(target, final_result)

        execution_time = time.time() - start_time
        
        # Track metrics
        self.metrics.append({
            "capability": capability,
            "execution_time": execution_time,
            "plugins_run": len(selected_adapters)
        })

        return {
            "capability": capability,
            "target": target,
            "results": final_result.dict(),
            "intelligence_graph": intelligence_graph,
            "execution_time": execution_time
        }

    def health_check(self):
        from core.registry.plugins.plugin_health import PluginHealthCheck
        return PluginHealthCheck.run_all_checks()

capability_manager = CapabilityManager()
