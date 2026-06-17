import yaml
import json
from pathlib import Path
from typing import Dict, Any
from reconx.core.workflow.task import Task
from reconx.core.workflow.dependency_graph import DependencyGraph
from reconx.core.workflow.scheduler import WorkflowScheduler
from reconx.core.workflow.result_aggregator import ResultAggregator
from reconx.core.workflow.execution_context import ExecutionContext
from reconx.core.workflow.event_bus import event_bus
from reconx.core.workflow.exceptions import WorkflowValidationError
from reconx.core.workflow.state_manager import StateManager
from reconx.core.database.session import async_session_factory


class WorkflowEngine:
    def __init__(self, workflows_dir: str = "src/reconx/workflows"):
        self.workflows_dir = Path(workflows_dir)

    def load_workflow(self, name: str) -> Dict[str, Any]:
        # Basic traversal security check
        if ".." in name or "/" in name or "\\" in name:
            raise WorkflowValidationError("Invalid workflow name")

        file_path = self.workflows_dir / f"{name}.yaml"
        if not file_path.exists():
            file_path = self.workflows_dir / "custom" / f"{name}.yaml"
            if not file_path.exists():
                raise WorkflowValidationError(f"Workflow {name} not found")

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if "name" not in data or "tasks" not in data:
            raise WorkflowValidationError("Workflow must contain 'name' and 'tasks'")

        return data

    async def execute_workflow(
        self, name: str, target: str, user_id: str = "system"
    ) -> Dict[str, Any]:
        workflow_def = self.load_workflow(name)

        tasks = []
        for t in workflow_def["tasks"]:
            tasks.append(
                Task(id=t["id"], plugin=t["plugin"], depends_on=t.get("depends_on", []))
            )

        graph = DependencyGraph(tasks)
        context = ExecutionContext(workflow_id=name, target=target, user=user_id)
        aggregator = ResultAggregator()

        async with async_session_factory() as db:
            state_manager = StateManager(db)
            exec_record = await state_manager.create_execution(name, target, user_id)

            await event_bus.publish(
                "WorkflowStarted", {"workflow_name": name, "target": target}
            )

            scheduler = WorkflowScheduler(graph, context, aggregator)
            await scheduler.run()

            summary = aggregator.get_summary()
            success = len(scheduler.failed) == 0

            # Stage 9: Intelligence Ingestion
            from reconx.core.intelligence.intelligence_store import IntelligenceStore

            intel_store = IntelligenceStore(db)
            await intel_store.ingest_plugin_result(
                project_id="default_proj",  # Hardcoded for now
                results={
                    "assets": summary.get("unique_assets", []),
                    "findings": aggregator.findings,
                },
            )

            status = "SUCCESS" if success else "FAILED"
            await state_manager.update_status(
                exec_record.id, status, json.dumps(summary)
            )

            event_type = "WorkflowCompleted" if success else "WorkflowFailed"
            await event_bus.publish(
                event_type,
                {"workflow_name": name, "target": target, "summary": summary},
            )

            return {
                "execution_id": exec_record.id,
                "status": status,
                "summary": summary,
                "tasks_completed": len(scheduler.completed),
                "tasks_failed": len(scheduler.failed),
            }


workflow_engine = WorkflowEngine()
