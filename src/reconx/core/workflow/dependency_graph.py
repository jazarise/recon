from typing import List, Dict
from reconx.core.workflow.task import Task, TaskStatus
from reconx.core.workflow.exceptions import (
    DependencyCycleError,
    WorkflowValidationError,
)


class DependencyGraph:
    def __init__(self, tasks: List[Task]):
        self.tasks = {t.id: t for t in tasks}
        self.graph: Dict[str, List[str]] = {t.id: [] for t in tasks}
        self.in_degree: Dict[str, int] = {t.id: 0 for t in tasks}
        self._build()

    def _build(self):
        for task in self.tasks.values():
            for dep in task.depends_on:
                if dep not in self.tasks:
                    raise WorkflowValidationError(
                        f"Task {task.id} depends on unknown task {dep}"
                    )
                self.graph[dep].append(task.id)
                self.in_degree[task.id] += 1

        # Detect cycles
        self._check_cycles()

    def _check_cycles(self):
        in_degree_copy = self.in_degree.copy()
        queue = [node for node, deg in in_degree_copy.items() if deg == 0]
        visited = 0

        while queue:
            node = queue.pop(0)
            visited += 1
            for neighbor in self.graph[node]:
                in_degree_copy[neighbor] -= 1
                if in_degree_copy[neighbor] == 0:
                    queue.append(neighbor)

        if visited != len(self.tasks):
            raise DependencyCycleError("Cycle detected in workflow tasks")

    def get_ready_tasks(self, completed: set, failed: set) -> List[Task]:
        ready = []
        for task in self.tasks.values():
            if task.status == "PENDING" or task.status == TaskStatus.PENDING:
                deps_met = all(dep in completed for dep in task.depends_on)
                deps_failed = any(dep in failed for dep in task.depends_on)

                if deps_failed:
                    task.status = TaskStatus.SKIPPED  # Enum will parse it ideally, but let's just let scheduler handle skipped
                elif deps_met:
                    ready.append(task)
        return ready
