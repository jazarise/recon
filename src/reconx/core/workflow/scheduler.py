import asyncio
from reconx.core.workflow.task import Task, TaskStatus
from reconx.core.workflow.dependency_graph import DependencyGraph
from reconx.core.workflow.result_aggregator import ResultAggregator
from reconx.core.workflow.execution_context import ExecutionContext
from reconx.core.workflow.event_bus import event_bus
from reconx.core.plugins.manager import plugin_manager
from reconx.core.database.session import async_session_factory
import datetime


class WorkflowScheduler:
    def __init__(
        self,
        graph: DependencyGraph,
        context: ExecutionContext,
        aggregator: ResultAggregator,
    ):
        self.graph = graph
        self.context = context
        self.aggregator = aggregator
        self.completed: set[str] = set()
        self.failed: set[str] = set()
        self.running_tasks: set[str] = set()

    async def execute_task(self, task: Task):
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.datetime.now(datetime.timezone.utc)
        await event_bus.publish("TaskStarted", {"task_id": task.id})

        retries_left = task.retries
        success = False

        while retries_left >= 0 and not success:
            try:
                # Execute plugin via plugin manager
                async with async_session_factory() as db:
                    result = await plugin_manager.execute_plugin(
                        db, task.plugin, "workflow_target", self.context.target
                    )

                if result.status == "success":
                    self.aggregator.add_result(task.id, result)
                    success = True
                    task.status = TaskStatus.SUCCESS
                    await event_bus.publish(
                        "TaskCompleted", {"task_id": task.id, "result": "success"}
                    )
                else:
                    retries_left -= 1
                    if retries_left < 0:
                        task.status = TaskStatus.FAILED
                        task.error = f"Plugin returned errors: {result.errors}"
                        await event_bus.publish(
                            "TaskFailed", {"task_id": task.id, "error": task.error}
                        )

            except Exception as e:
                retries_left -= 1
                if retries_left < 0:
                    task.status = TaskStatus.FAILED
                    task.error = str(e)
                    await event_bus.publish(
                        "TaskFailed", {"task_id": task.id, "error": task.error}
                    )

        task.finished_at = datetime.datetime.now(datetime.timezone.utc)

        if task.status == TaskStatus.SUCCESS:
            self.completed.add(task.id)
        else:
            self.failed.add(task.id)

        self.running_tasks.remove(task.id)

    async def run(self):
        while len(self.completed) + len(self.failed) < len(self.graph.tasks):
            ready_tasks = self.graph.get_ready_tasks(self.completed, self.failed)

            # Any task that was implicitly skipped by graph needs to be added to failed/skipped
            for task_id, task in self.graph.tasks.items():
                if task.status == TaskStatus.SKIPPED and task_id not in self.failed:
                    self.failed.add(task.id)

            tasks_to_schedule = []
            for t in ready_tasks:
                if t.id not in self.running_tasks:
                    self.running_tasks.add(t.id)
                    tasks_to_schedule.append(self.execute_task(t))

            if not tasks_to_schedule and self.running_tasks:
                # Wait for at least one running task to finish to unblock
                await asyncio.sleep(0.1)
                continue
            elif not tasks_to_schedule and not self.running_tasks:
                # Deadlock or all done/skipped
                break

            if tasks_to_schedule:
                # Run tasks in parallel
                await asyncio.gather(*tasks_to_schedule)
