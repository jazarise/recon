import time
from reconx.core.models import AdapterResult
from typing import Any

class PluginSandbox:
    """Safely executes a plugin adapter, isolating failures from crashing the orchestration."""

    @staticmethod
    def execute(adapter_instance: Any, target: str, timeout_seconds: int = 30) -> AdapterResult:
        """
        Executes an adapter inside a try/catch safety wrapper.
        For MVP, we use basic exception handling. In a full system, this could
        use multiprocessing with strict memory and CPU cgroups.
        """
        start_time = time.time()
        
        try:
            # 1. Validation
            if not adapter_instance.validate(target=target):
                print(f"[-] Sandbox: Adapter rejected validation for target {target}")
                return AdapterResult()

            # 2. Execution (In a real scenario, this would be wrapped in a threading.Timer or asyncio timeout)
            # We assume the adapters themselves respect the timeout param.
            raw_output = adapter_instance.execute(target=target)
            
            # 3. Normalization
            result: AdapterResult = adapter_instance.normalize(raw_output)
            
            return result
            
        except Exception as e:
            # Prevent the plugin failure from crashing the entire correlation run
            print(f"[-] Sandbox execution failed: {e}")
            return AdapterResult()
