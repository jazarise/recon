import asyncio
from typing import Callable, Dict, Any

class AsmScheduler:
    """Manages continuous/recurring jobs."""
    def __init__(self):
        self.jobs: Dict[str, asyncio.Task] = {}

    def schedule_job(self, name: str, interval_seconds: int, func: Callable, *args, **kwargs):
        async def job_loop():
            while True:
                try:
                    # Run synchronously or asynchronously based on the function
                    if asyncio.iscoroutinefunction(func):
                        await func(*args, **kwargs)
                    else:
                        loop = asyncio.get_running_loop()
                        await loop.run_in_executor(None, func, *args, **kwargs)
                except Exception as e:
                    print(f"[-] Scheduled job '{name}' failed: {e}")
                
                await asyncio.sleep(interval_seconds)

        loop = asyncio.get_running_loop()
        task = loop.create_task(job_loop())
        self.jobs[name] = task
        print(f"[+] Scheduled job '{name}' every {interval_seconds}s")

    def cancel_job(self, name: str):
        if name in self.jobs:
            self.jobs[name].cancel()
            del self.jobs[name]
            print(f"[-] Cancelled job '{name}'")

asm_scheduler = AsmScheduler()
