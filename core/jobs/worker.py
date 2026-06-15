import asyncio
from core.jobs.queue import job_queue
from core.observability.metrics import metrics

class JobWorker:
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.running = False
        
    async def start(self):
        self.running = True
        print(f"[WORKER {self.worker_id}] Started and waiting for jobs...")
        
        while self.running:
            try:
                priority, job = await asyncio.wait_for(job_queue.queue.get(), timeout=1.0)
                await self.process_job(job)
                job_queue.queue.task_done()
            except asyncio.TimeoutError:
                continue
                
    async def process_job(self, job: dict):
        print(f"[WORKER {self.worker_id}] Processing Job {job['id']} -> {job['capability']} on {job['target']}")
        
        start_time = asyncio.get_running_loop().time()
        
        # Simulate execution
        from core.capabilities import capability_manager
        
        # Run capability in a thread pool to avoid blocking the async worker
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, capability_manager.run, job['capability'], job['target'])
        
        duration = asyncio.get_running_loop().time() - start_time
        metrics.record_scan(job['capability'], duration)
        
        print(f"[WORKER {self.worker_id}] Completed Job {job['id']} in {duration:.2f}s")
        
    def stop(self):
        self.running = False
