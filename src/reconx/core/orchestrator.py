import asyncio
import uuid
import importlib
import json
import os
from pathlib import Path

from reconx.core.workflow_engine import workflow_engine, WorkflowContext
from reconx.core.logger import logger
from reconx.core.event_bus import event_bus
from reconx.core.errors import PluginError
from reconx.core.models.scan import Scan

ROOT = Path(__file__).parent.parent

class Orchestrator:
    def __init__(self):
        self.running_scans = {}
        self.plugin_map = {}
        self._load_registry()

    def _load_registry(self):
        reg_path = ROOT / "core" / "plugin_registry.json"
        if reg_path.exists():
            try:
                with open(reg_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for p in data:
                        # Extract the module path from the file path
                        # e.g., plugins\recon\activity_feed\plugin.py -> plugins.recon.activity_feed.plugin
                        p_path = p.get("path", "")
                        if p_path.endswith(".py"):
                            mod_path = p_path[:-3].replace("\\", ".").replace("/", ".")
                            # Use plugin id or name as key
                            pid = p.get("id") or p.get("name")
                            if pid:
                                self.plugin_map[pid] = mod_path
            except Exception as e:
                logger.error(f"Failed to load plugin registry: {e}")

    def get_plugin_module(self, plugin_name: str):
        """Dynamically imports a plugin given its string name."""
        mod_path = self.plugin_map.get(plugin_name)
        if not mod_path:
            # Fallback for dynamic discovery if not in registry
            # Search dynamically
            logger.warning(f"Plugin {plugin_name} not found in registry, attempting fallback.")
            return None
            
        try:
            return importlib.import_module(mod_path)
        except Exception as e:
            logger.warning(f"Failed to import plugin {plugin_name} at {mod_path}: {e}")
            return None

    async def execute_plugin(self, plugin_name: str, context: WorkflowContext, max_retries: int = 3):
        event_bus.emit("PluginStarted", plugin=plugin_name, target=context.target)
        logger.info(f"Executing plugin: {plugin_name}")
        
        attempt = 0
        while attempt < max_retries:
            try:
                module = self.get_plugin_module(plugin_name)
                if not module or not hasattr(module, "run"):
                    raise PluginError(f"Plugin {plugin_name} could not be loaded or missing 'run' method.")
                
                # Execute standard async run interface
                results = await module.run(context.target, {"target": context.target})
                
                # We expect dict: {"success": bool, "plugin": str, "category": str, "data": ...}
                if isinstance(results, dict):
                    if results.get("success"):
                        context.findings.append(results)
                        event_bus.emit("FindingCreated", finding=results.get("category", "unknown"), value=results.get("data"))
                        event_bus.emit("PluginFinished", plugin=plugin_name, target=context.target)
                        return True
                    else:
                        raise PluginError(f"Plugin reported failure: {results.get('errors')}")
                else:
                    raise PluginError(f"Plugin returned invalid schema: {type(results)}")
                    
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
        
        import time
        scan_model = Scan(target=target, workflow=workflow_name, status="running", started_at=time.time())
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

        import time
        scan_model.status = "completed"
        scan_model.finished_at = time.time()
        event_bus.emit("WorkflowCompleted", scan_id=scan_id, total_findings=len(context.findings))
        
        return context

orchestrator = Orchestrator()
