import queue
from core.logger import logger

class TaskQueue:
    def __init__(self):
        self._q = queue.Queue()

    def enqueue(self, task):
        self._q.put(task)
        logger.debug(f"Task enqueued: {task}")

    def dequeue(self):
        if not self._q.empty():
            task = self._q.get()
            logger.debug(f"Task dequeued: {task}")
            return task
        return None

    def is_empty(self):
        return self._q.empty()

# Basic in-memory queue. In the future this will be replaced with SQLite or Redis.
task_queue = TaskQueue()
