import asyncio
import logging
import random

logger = logging.getLogger("reconx")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
]

class StealthHTTPClient:
    def __init__(self, mode: str = "normal"):
        self.mode = mode
        
    async def fetch(self, url: str):
        # UA Rotation
        ua = random.choice(USER_AGENTS) if self.mode == "stealth" else USER_AGENTS[0]
        
        # Jitter Injection
        if self.mode == "stealth":
            jitter = random.uniform(0.2, 1.5)
            logger.debug(f"[STEALTH] Sleeping for {jitter:.2f}s before request...")
            await asyncio.sleep(jitter)
            
        logger.info(f"Fetching {url} [UA: {ua[:30]}...]")
        # Simulated Network Call
        await asyncio.sleep(0.1)
        return {"status": 200, "url": url}
