import asyncio
import logging
from src.reconx.distributed.queue import JobQueue
from src.reconx.distributed.aggregator import CentralAggregator
from src.reconx.distributed.messaging import MessageBroker

logger = logging.getLogger("reconx")

class MasterNode:
    def __init__(self):
        self.queue = JobQueue()
        self.aggregator = CentralAggregator()
        self.broker = MessageBroker()
        
        self.broker.subscribe("DATA_RETURNED", self.aggregator.process_worker_data)
        self.broker.subscribe("TASK_FAILED", self.handle_worker_failure)

    async def handle_worker_failure(self, data: dict):
        job_id = data.get("job_id")
        target = data.get("target")
        task = data.get("task")
        logger.error(f"[MASTER] Fault Tolerance triggered. Re-queueing job {job_id} for {target}")
        await self.queue.push(target, task, priority="high")

    async def dispatch_campaign(self, targets: list):
        for target in targets:
            await self.queue.push(target, "subdomain_enum")
            await self.queue.push(target, "port_scan")
            await self.queue.push(target, "tech_detect")
            
        logger.warning(f"[MASTER] Bootstrapped campaign across {len(targets)} targets. Job Queue populated.")
        
        # Start broker listener in background
        asyncio.create_task(self.broker.run_listener())
