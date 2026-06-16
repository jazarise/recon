from enum import Enum
from reconx.core.logger import logger
from typing import Dict, Any

class TaskState(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Any] = {}

    def create_task(self, task_id: str, payload: Any):
        self.tasks[task_id] = {
            "status": TaskState.PENDING,
            "payload": payload,
            "retries": 0
        }
        logger.info(f"Task {task_id} created.")

    def update_status(self, task_id: str, status: TaskState):
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status
            logger.info(f"Task {task_id} changed status to {status.value}")
        else:
            logger.error(f"Cannot update status. Task {task_id} not found.")

    def get_task(self, task_id: str):
        return self.tasks.get(task_id)

task_manager = TaskManager()
