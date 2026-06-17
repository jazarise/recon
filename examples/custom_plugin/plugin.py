from reconx.core.plugins import ReconPlugin


class CustomPlugin(ReconPlugin):
    async def execute(self, target):
        return {"status": "success"}
