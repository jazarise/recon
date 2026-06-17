import asyncio
from typing import Coroutine, Any
from reconx.core.reconx.utils.logger import logger

class AsyncExecutor:
    """Manages execution of tasks using asyncio.TaskGroup."""
    
    def __init__(self):
        self._running_tasks = set()

    async def execute_all(self, tasks: list[Coroutine]) -> list[Any]:
        """Execute a list of coroutines concurrently using a TaskGroup."""
        results = []
        try:
            async with asyncio.TaskGroup() as tg:
                # We need a wrapper to capture results since TaskGroup tasks 
                # don't return values directly when awaited via gather in tg
                async def _wrapper(coro):
                    res = await coro
                    results.append(res)
                    return res
                
                for task in tasks:
                    tg.create_task(_wrapper(task))
            
            logger.debug(f"Successfully executed {len(tasks)} tasks.")
            return results
        except ExceptionGroup as eg:
            logger.error("Errors occurred during task execution.", exc_info=eg)
            raise

    async def run_in_background(self, coro: Coroutine):
        """Run a task in the background."""
        task = asyncio.create_task(coro)
        self._running_tasks.add(task)
        task.add_done_callback(self._running_tasks.discard)
