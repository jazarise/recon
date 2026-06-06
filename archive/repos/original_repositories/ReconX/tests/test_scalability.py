import asyncio
import sys
import os
import time

sys.path.append("e:/ReconX")

from events.event_bus import EventBus
from core.workflow_engine import WorkflowEngine
from core.plugin_loader import PluginLoader
from core.execution_manager import ExecutionManager
from core.orchestrator import Orchestrator
from core.result_store import ResultStore

async def test_scalability():
    print("Initializing Orchestrator for Scalability Test...")
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
    
    await orchestrator.start()
    
    wf_path = "e:/ReconX/golden_workflow.yaml"
    if not os.path.exists(wf_path):
        print(f"ERROR: {wf_path} not found. Ensure Stage 17 was completed.")
        sys.exit(1)

    print(f"Launching 10 concurrent executions of the Golden Workflow...")
    start_time = time.time()
    
    tasks = []
    for i in range(10):
        target = f"test-target-{i}.internal"
        tasks.append(orchestrator.run_workflow(wf_path, target=target))
        
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    
    success_count = sum(1 for r in results if r["status"] == "completed")
    print(f"\n--- Scalability Test Results ---")
    print(f"Total Workflows: 10")
    print(f"Successful: {success_count}")
    print(f"Time Taken: {end_time - start_time:.2f} seconds")
    
    assert success_count == 10, f"Expected 10 successes, got {success_count}"
    print("SCALABILITY VALIDATION: SUCCESS")

if __name__ == "__main__":
    asyncio.run(test_scalability())
