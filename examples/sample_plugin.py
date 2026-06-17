from sdk.plugin_sdk import ReconXPlugin, validate_target, run_command


class NmapPlugin(ReconXPlugin):
    @property
    def name(self) -> str:
        return "nmap_fast"

    @property
    def version(self) -> str:
        return "1.0.0"

    async def execute(self, target: str, **kwargs) -> str:
        if not validate_target(target):
            raise ValueError("Invalid target")
        return await run_command(["nmap", "-F", target])

    def parse(self, output: str) -> list:
        # Example parsing logic
        return [{"type": "asset", "value": output}]
