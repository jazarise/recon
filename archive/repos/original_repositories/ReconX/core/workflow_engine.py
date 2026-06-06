"""
ReconX WorkflowEngine — YAML-based workflow loading and execution.
"""

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class WorkflowEngine:
    """Load workflow definitions from YAML and execute their steps."""

    def __init__(self, execution_manager: Any, event_bus: Any) -> None:
        self.execution_manager = execution_manager
        self.event_bus = event_bus
        self._runs: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # load
    # ------------------------------------------------------------------
    def load_workflow(self, path: str) -> Dict[str, Any]:
        """Parse a YAML workflow file and return its definition dict."""
        workflow_path = Path(path)
        if not workflow_path.exists():
            raise FileNotFoundError(f"Workflow file not found: {path}")

        with open(workflow_path, "r", encoding="utf-8") as fh:
            workflow = yaml.safe_load(fh)

        if not isinstance(workflow, dict):
            raise ValueError(f"Invalid workflow format in {path}")
        return workflow

    # ------------------------------------------------------------------
    # execute
    # ------------------------------------------------------------------
    async def execute(
        self,
        workflow: Dict[str, Any],
        target: str,
        workflow_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run every step in *workflow* against *target*.

        Returns a result dict with step outcomes.
        """
        wf_id = workflow_id or str(uuid.uuid4())
        run_record: Dict[str, Any] = {
            "workflow_id": wf_id,
            "workflow_name": workflow.get("name", "unnamed"),
            "target": target,
            "status": "running",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": None,
            "steps": [],
        }
        self._runs[wf_id] = run_record

        await self.event_bus.publish("workflow.started", {
            "workflow_id": wf_id,
            "workflow_name": run_record["workflow_name"],
            "target": target,
        })

        steps = workflow.get("steps", workflow.get("stages", []))
        
        # Initialize execution context with target
        execution_context = {"target": target, "findings": []}
        
        for step in steps:
            step_id = step.get("id", str(uuid.uuid4()))
            plugin_name = step.get("plugin", "unknown")
            await self.event_bus.publish("step.started", {
                "workflow_id": wf_id,
                "step_id": step_id,
                "plugin": plugin_name,
            })

            step_result = {
                "step_id": step_id,
                "plugin": plugin_name,
                "status": "completed",
                "started_at": datetime.now(timezone.utc).isoformat(),
                "completed_at": None,
                "output": None,
            }

            try:
                # Delegate to ExecutionManager if the adapter is available
                output = await self.execution_manager.execute_step(step, target, execution_context)
                step_result["output"] = output
                step_result["status"] = "completed"
                
                # Merge outputs back into the global context for the next step
                if output and isinstance(output, dict) and "findings" in output:
                    execution_context["findings"].extend(output.get("findings", []))
                execution_context[plugin_name] = output

            except Exception as exc:
                step_result["status"] = "failed"
                step_result["error"] = str(exc)

            step_result["completed_at"] = datetime.now(timezone.utc).isoformat()
            run_record["steps"].append(step_result)

            await self.event_bus.publish("step.completed", {
                "workflow_id": wf_id,
                "step_id": step_id,
                "status": step_result["status"],
            })

        run_record["status"] = "completed"
        run_record["completed_at"] = datetime.now(timezone.utc).isoformat()
        run_record["final_context"] = execution_context

        await self.event_bus.publish("workflow.completed", {
            "workflow_id": wf_id,
            "status": "completed",
        })

        return run_record

    # ------------------------------------------------------------------
    # status
    # ------------------------------------------------------------------
    def get_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Return the run record for *workflow_id*, or ``None``."""
        return self._runs.get(workflow_id)

    @property
    def runs(self) -> Dict[str, Dict[str, Any]]:
        return dict(self._runs)
