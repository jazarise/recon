import asyncio
import sys
import yaml
import os

from pathlib import Path
import sys

# Compute project root relative to this test file
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from events.event_bus import EventBus
from core.workflow_engine.engine import WorkflowEngine
from core.plugin_manager.loader import PluginManager
from core.engine.execution_manager import ExecutionManager
from core.engine.orchestrator import Orchestrator
from core.result_store import ResultStore

async def main():
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
    
    # Listen to events to verify execution
    events_received = []
    def log_event(ename):
        async def handler(payload):
            events_received.append((ename, payload))
            print(f"[EVENT] {ename} -> {payload.get('plugin', payload.get('workflow_name', ''))}")
        return handler
        
    for e in ["workflow.started", "plugin_started", "plugin_completed", "plugin_failed", "workflow.completed"]:
        event_bus.subscribe(e, log_event(e))
        
    # Write the workflow yaml
    wf_path = str(ROOT / "golden_workflow.yaml")
    wf_def = {
        "name": "Golden Recon Workflow",
        "steps": [
            {"id": "s1", "plugin": "network_discovery", "plugin_path": "plugins/golden/network_discovery", "timeout": 30},
            {"id": "s2", "plugin": "web_recon", "plugin_path": "plugins/golden/web_recon", "timeout": 30},
            {"id": "s3", "plugin": "dns_intelligence", "plugin_path": "plugins/golden/dns_intelligence", "timeout": 30},
            {"id": "s4", "plugin": "llm_analysis", "plugin_path": "plugins/golden/llm_analysis", "timeout": 30},
            {"id": "s5", "plugin": "reporting", "plugin_path": "plugins/golden/reporting", "timeout": 30}
        ]
    }
    
    with open(wf_path, "w") as f:
        yaml.dump(wf_def, f)
        
    print("Executing Golden Workflow against google.com...")
    await orchestrator.start()
    result = await orchestrator.run_workflow(wf_path, target="google.com")
    
    # Assertions
    assert result["status"] == "completed"
    assert "final_context" in result
    
    ctx = result["final_context"]
    assert "network_discovery" in ctx
    assert "web_recon" in ctx
    assert "dns_intelligence" in ctx
    assert "llm_analysis" in ctx
    assert "reporting" in ctx
    
    assert ctx["reporting"]["plugin"] == "reporting"
    assert "report_path" in ctx["reporting"]
    
    report_path = ctx["reporting"]["report_path"]
    assert os.path.exists(report_path)
    
    print(f"\nSUCCESS! Multi-plugin workflow executed. Report generated at {report_path}")
    print("Reading first 15 lines of the report:")
    with open(report_path, "r") as f:
        print("".join(f.readlines()[:15]))
        
if __name__ == "__main__":
    asyncio.run(main())
