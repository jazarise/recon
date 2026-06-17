import asyncio
import logging
import random
from reconx.distributed.queue import JobQueue
from reconx.distributed.messaging import MessageBroker

logger = logging.getLogger("reconx")

class WorkerNode:
    def __init__(self, worker_id: str, queue: JobQueue):
        self.worker_id = worker_id
        self.queue = queue
        self.broker = MessageBroker()

    async def work_loop(self):
        logger.info(f"[WORKER-{self.worker_id}] Online and listening for jobs.")
        while True:
            job = await self.queue.pop()
            logger.info(f"[WORKER-{self.worker_id}] Executing Job: {job.task} on {job.target}")
            
            await asyncio.sleep(0.5) # Simulate workload
            
            # Simulate 10% failure rate for Fault Tolerance
            if random.random() < 0.1:
                logger.error(f"[WORKER-{self.worker_id}] Task crashed! Emitting TASK_FAILED.")
                await self.broker.publish("TASK_FAILED", job.model_dump())
            else:
                simulated_findings = [f"node-{random.randint(1,100)}.{job.target}"]
                await self.broker.publish("DATA_RETURNED", {"target": job.target, "results": simulated_findings})
                
            self.queue.mark_completed(job.job_id)
