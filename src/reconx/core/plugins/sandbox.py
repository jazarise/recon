import asyncio
from reconx.core.plugins.base import ReconXPlugin, PluginResult
from reconx.core.plugins.exceptions import PluginTimeoutError, PluginExecutionError


class PluginSandbox:
    def __init__(self, timeout: int = 300):
        self.timeout = timeout

    async def execute(self, plugin: ReconXPlugin, target: str) -> PluginResult:
        try:
            return await asyncio.wait_for(plugin.execute(target), timeout=self.timeout)
        except asyncio.TimeoutError:
            raise PluginTimeoutError(
                f"Plugin {plugin.name} timed out after {self.timeout}s"
            )
        except Exception as e:
            raise PluginExecutionError(f"Plugin {plugin.name} failed: {e}")
