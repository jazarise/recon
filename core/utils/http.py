import aiohttp
from typing import Optional, Dict, Any

class HttpClient:
    def __init__(self, timeout: int = 10, user_agent: str = "ReconX/2.0.0"):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.headers = {"User-Agent": user_agent}

    async def get(self, url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession(timeout=self.timeout, headers=self.headers) as session:
                async with session.get(url, params=params) as response:
                    return {
                        "status": response.status,
                        "text": await response.text(),
                        "url": str(response.url)
                    }
        except Exception as e:
            return {"status": 0, "error": str(e)}

    async def post(self, url: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession(timeout=self.timeout, headers=self.headers) as session:
                async with session.post(url, data=data) as response:
                    return {
                        "status": response.status,
                        "text": await response.text(),
                        "url": str(response.url)
                    }
        except Exception as e:
            return {"status": 0, "error": str(e)}
