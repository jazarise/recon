import asyncio
from typing import Dict, Any
from core.correlation_engine import CorrelationEngine
from core.database import DatabaseManager

class Orchestrator:
    def __init__(self, event_bus, workflow_engine, execution_manager, result_store=None):
        self.event_bus = event_bus
        self.workflow_engine = workflow_engine
        self.execution_manager = execution_manager
        self.result_store = result_store

    async def start(self):
        print("ReconX Orchestrator initializing...")
        await self.event_bus.publish("orchestrator.started", {})

    async def run_workflow(self, workflow_path: str, target: str, project_name: str = "default"):
        workflow = self.workflow_engine.load_workflow(workflow_path)
        
        result = await self.workflow_engine.execute(workflow, target)
        
        if self.result_store:
            # Ensure the result store is pointing to the correct project workspace
            self.result_store.project_name = project_name
            await self.result_store.save_result(result["workflow_id"], result)
            
            # Run Intelligence Correlation
            db_manager = DatabaseManager(project_name)
            correlation_engine = CorrelationEngine(db_manager)
            print(f"[*] Correlating findings for project: {project_name}...")
            await correlation_engine.correlate(result)
            
        return result
