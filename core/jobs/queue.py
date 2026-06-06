import asyncio
from typing import Dict

class JobQueue:
    def __init__(self):
        self.queue = asyncio.PriorityQueue()
        
    async def submit_job(self, job_id: str, capability: str, target: str, priority: int = 1):
        job = {
            "id": job_id,
            "capability": capability,
            "target": target
        }
        # Lower number = higher priority
        await self.queue.put((priority, job))
        print(f"[JOB QUEUE] Submitted Job {job_id} ({capability} on {target}) with priority {priority}")

job_queue = JobQueue()
