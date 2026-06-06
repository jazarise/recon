import asyncio
import uuid
import importlib
from typing import Optional
from core.workflow_engine import workflow_engine, WorkflowContext
from core.logger import logger
from core.event_bus import event_bus
from core.errors import PluginError
from core.models.scan import Scan

class Orchestrator:
    def __init__(self):
        self.running_scans = {}

    def get_plugin_instance(self, plugin_name: str):
        """Dynamically imports a plugin given its string name."""
        search_paths = [
            f"modules.recon.{plugin_name}.plugin",
            f"modules.osint.{plugin_name}.plugin",
            f"modules.ai.{plugin_name}.plugin",
        ]
        for path in search_paths:
            try:
                module = importlib.import_module(path)
                return getattr(module, "Plugin")()
            except (ImportError, AttributeError):
                continue
        logger.warning(f"Plugin {plugin_name} not found dynamically.")
        return None

    async def execute_plugin(self, plugin_name: str, context: WorkflowContext, max_retries: int = 3):
        event_bus.emit("PluginStarted", plugin=plugin_name, target=context.target)
        logger.info(f"Executing plugin: {plugin_name}")
        
        attempt = 0
        while attempt < max_retries:
            try:
                instance = self.get_plugin_instance(plugin_name)
                if not instance:
                    raise PluginError(f"Plugin {plugin_name} could not be loaded.")
                
                # Execute logic
                if hasattr(instance, "execute"):
                    if asyncio.iscoroutinefunction(instance.execute):
                        results = await instance.execute(context.target)
                    else:
                        results = await asyncio.to_thread(instance.execute, context.target)
                        
                    context.findings.extend(results)
                    for f in results:
                        event_bus.emit("FindingCreated", finding=f.category, value=f.value)
                
                event_bus.emit("PluginFinished", plugin=plugin_name, target=context.target)
                return True
            except Exception as e:
                attempt += 1
                logger.warning(f"Plugin {plugin_name} failed (Attempt {attempt}/{max_retries}): {e}")
                if attempt >= max_retries:
                    logger.error(f"Plugin {plugin_name} exhausted retries. Failing gracefully.")
                    event_bus.emit("PluginFailed", plugin=plugin_name, error=str(e))
                    return False
                await asyncio.sleep(2 ** attempt) # Exponential backoff

    async def run_workflow(self, workflow_name: str, target: str):
        workflow_engine.validate_workflow(workflow_name)
        sorter, all_plugins = workflow_engine.build_execution_graph(workflow_name)
        
        scan_id = str(uuid.uuid4())
        context = WorkflowContext(target=target, scan_id=scan_id)
        
        scan_model = Scan(target=target, workflow=workflow_name)
        self.running_scans[scan_id] = scan_model
        
        event_bus.emit("ScanStarted", scan_id=scan_id, target=target, workflow=workflow_name)
        
        sorter.prepare()
        tasks = {}
        
        while sorter.is_active():
            for node in sorter.get_ready():
                task = asyncio.create_task(self.execute_plugin(node, context))
                tasks[task] = node
                
            if not tasks:
                break
                
            done, pending = await asyncio.wait(tasks.keys(), return_when=asyncio.FIRST_COMPLETED)
            
            for t in done:
                node = tasks.pop(t)
                sorter.done(node)

        scan_model.status = "completed"
        scan_model.findings = context.findings
        event_bus.emit("WorkflowCompleted", scan_id=scan_id, total_findings=len(context.findings))
        
        return context

orchestrator = Orchestrator()
