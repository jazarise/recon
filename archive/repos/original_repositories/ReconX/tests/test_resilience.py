import asyncio
import sys
import yaml
import os

sys.path.append("e:/ReconX")

from events.event_bus import EventBus
from core.workflow_engine import WorkflowEngine
from core.plugin_loader import PluginLoader
from core.execution_manager import ExecutionManager
from core.orchestrator import Orchestrator
from core.result_store import ResultStore

async def test_resilience():
    event_bus = EventBus()
    plugin_loader = PluginLoader(base_path="e:/ReconX")
    execution_manager = ExecutionManager(event_bus=event_bus, plugin_loader=plugin_loader)
    workflow_engine = WorkflowEngine(execution_manager=execution_manager, event_bus=event_bus)
    result_store = ResultStore(base_dir="e:/ReconX/outputs")
    
    orchestrator = Orchestrator(
        event_bus=event_bus, 
        workflow_engine=workflow_engine, 
        execution_manager=execution_manager,
        result_store=result_store
    )
    
    # 1. Test Plugin Crash Containment
    wf_crash_path = "e:/ReconX/wf_crash.yaml"
    with open(wf_crash_path, "w") as f:
        yaml.dump({
            "name": "Crash Workflow",
            "steps": [{"id": "s1", "plugin": "malicious", "plugin_path": "plugins/golden/malicious", "config": {"mode": "crash"}, "timeout": 5}]
        }, f)
        
    print("Testing Plugin Crash Containment...")
    await orchestrator.start()
    res1 = await orchestrator.run_workflow(wf_crash_path, target="localhost")
    assert res1["status"] == "completed"  # The workflow engine successfully completed the attempt
    assert res1["steps"][0]["status"] == "failed"
    print("Error was:", res1["steps"][0]["error"])
    assert "Simulated memory corruption" in res1["steps"][0]["error"] or "MemoryError" in res1["steps"][0]["error"]
    print("Crash containment SUCCESS: Orchestrator survived exception.\n")
    
    # 2. Test Infinite Loop Containment
    wf_hang_path = "e:/ReconX/wf_hang.yaml"
    with open(wf_hang_path, "w") as f:
        yaml.dump({
            "name": "Hang Workflow",
            "steps": [{"id": "s2", "plugin": "malicious", "plugin_path": "plugins/golden/malicious", "config": {"mode": "infinite_loop"}, "timeout": 2}]
        }, f)
        
    print("Testing Infinite Loop Hard Timeout Containment...")
    res2 = await orchestrator.run_workflow(wf_hang_path, target="localhost")
    assert res2["status"] == "completed"
    assert res2["steps"][0]["status"] == "failed"
    assert "timed out after 2s and was forcibly terminated" in res2["steps"][0]["error"]
    print("Timeout containment SUCCESS: Subprocess forcibly killed after 2 seconds.\n")

if __name__ == "__main__":
    asyncio.run(test_resilience())
