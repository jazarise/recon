from core.http.client import HttpClient
import time


class Plugin:
    name = 'malicious'
    category = 'recon'
    async def run(target: str, context: dict) -> dict -> dict:
        mode = config.get("mode", "crash")
        
        if mode == "crash":
            raise MemoryError("Simulated memory corruption or segfault")
            
        if mode == "infinite_loop":
            # Simulate a blocking C-extension or unyielding while loop
            # This should trigger the ExecutionManager hard timeout
            while True:
                time.sleep(1)
                
        return {"plugin": "malicious", "status": "survived"}
