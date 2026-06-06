from core.workflow_engine.engine import WorkflowEngine
from core.paths import WORKFLOWS_DIR
import json

engine = WorkflowEngine(execution_manager=None, event_bus=None)

try:
    workflow = engine.load_workflow(WORKFLOWS_DIR / "basic.yaml")
    print(json.dumps(workflow, indent=2))
except Exception as e:
    print(f"Failed to load workflow: {e}")
