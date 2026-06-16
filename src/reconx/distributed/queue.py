from pydantic import BaseModel
import uuid
import asyncio

class ReconJob(BaseModel):
    job_id: str
    target: str
    task: str
    priority: str = "normal"

class JobQueue:
    def __init__(self):
        self._queue = asyncio.PriorityQueue()
        self._in_flight = {}
        
    async def push(self, target: str, task: str, priority: str = "normal"):
        job = ReconJob(job_id=str(uuid.uuid4()), target=target, task=task, priority=priority)
        weight = 1 if priority == "high" else 5
        await self._queue.put((weight, job))
        
    async def pop(self) -> ReconJob:
        _, job = await self._queue.get()
        self._in_flight[job.job_id] = job
        return job

    def mark_completed(self, job_id: str):
        if job_id in self._in_flight:
            del self._in_flight[job_id]
            self._queue.task_done()
            
    def get_in_flight(self) -> list:
        return list(self._in_flight.values())
