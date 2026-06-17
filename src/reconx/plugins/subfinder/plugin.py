from reconx.core.plugins.base import ReconXPlugin, PluginResult
from reconx.integrations.subfinder import SubfinderAdapter


class SubfinderPlugin(ReconXPlugin):
    async def validate(self) -> bool:
        # We could check if subfinder is in PATH here
        return True

    async def execute(self, target: str) -> PluginResult:
        try:
            findings = SubfinderAdapter.run_subfinder(target)
            return PluginResult(
                status="success",
                findings=findings,
                assets=[
                    {"type": "domain", "value": f.get("host", target)} for f in findings
                ],
            )
        except Exception as e:
            return PluginResult(status="error", errors=[str(e)])

    async def cleanup(self) -> None:
        pass

def register():
    return SubfinderPlugin
