import asyncio
import sys
import yaml
import os

from pathlib import Path
import sys
import tempfile
import textwrap

# Compute project root relative to this test file
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def _write_crash_plugin(tmp_dir: str) -> str:
    adapter_dir = Path(tmp_dir) / "crash_plugin"
    adapter_dir.mkdir()
    (adapter_dir / "adapter.py").write_text(textwrap.dedent("""
        import time
        from core.plugin_manager.interface import PluginInterface
        class ToolAdapter(PluginInterface):
            async def execute(self, config, context):
                if config.get("mode") == "crash":
                    raise MemoryError("Simulated memory corruption")
                elif config.get("mode") == "infinite_loop":
                    while True:
                        time.sleep(1)
    """))
    return str(adapter_dir.relative_to(ROOT))

from events.event_bus import EventBus
from core.workflow_engine.engine import WorkflowEngine
from core.plugin_manager.loader import PluginManager
from core.engine.execution_manager import ExecutionManager
from core.engine.orchestrator import Orchestrator
from core.result_store import ResultStore

async def test_resilience():
    event_bus = EventBus()
    plugin_loader = PluginManager()
    execution_manager = ExecutionManager(event_bus=event_bus, plugin_loader=plugin_loader)
    workflow_engine = WorkflowEngine(execution_manager=execution_manager, event_bus=event_bus)
    result_store = ResultStore(project_name="test_project")
    
    orchestrator = Orchestrator(
        event_bus=event_bus, 
        workflow_engine=workflow_engine, 
        execution_manager=execution_manager,
        result_store=result_store
    )
    
    # 1. Test Plugin Crash Containment
    with tempfile.TemporaryDirectory() as tmp_dir:
        crash_plugin_path = _write_crash_plugin(tmp_dir)
        wf_crash_path = str(ROOT / "wf_crash.yaml")
        with open(wf_crash_path, "w") as f:
            yaml.dump({
                "name": "Crash Workflow",
                "steps": [{"id": "s1", "plugin": "malicious", "plugin_path": crash_plugin_path, "config": {"mode": "crash"}, "timeout": 5}]
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
    wf_hang_path = str(ROOT / "wf_hang.yaml")
    with open(wf_hang_path, "w") as f:
        yaml.dump({
            "name": "Hang Workflow",
            "steps": [{"id": "s2", "plugin": "malicious", "plugin_path": crash_plugin_path, "config": {"mode": "infinite_loop"}, "timeout": 2}]
        }, f)
        
    print("Testing Infinite Loop Hard Timeout Containment...")
    res2 = await orchestrator.run_workflow(wf_hang_path, target="localhost")
    assert res2["status"] == "completed"
    assert res2["steps"][0]["status"] == "failed"
    assert "timed out after 2s and was forcibly terminated" in res2["steps"][0]["error"]
    print("Timeout containment SUCCESS: Subprocess forcibly killed after 2 seconds.\n")

if __name__ == "__main__":
    asyncio.run(test_resilience())
