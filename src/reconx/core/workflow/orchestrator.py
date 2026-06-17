from reconx.core.workflow.workflow_engine import workflow_engine


# Alias orchestrator to workflow engine for backward compatibility if needed,
# or keep them combined. The prompt asks for orchestrator.py too.
class Orchestrator:
    async def run(self, name: str, target: str):
        return await workflow_engine.execute_workflow(name, target)


orchestrator = Orchestrator()
