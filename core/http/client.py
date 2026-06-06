import aiohttp
from typing import Optional, Any

class HttpClient:
    def __init__(self, timeout: int = 10):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def request(self, method: str, url: str, **kwargs) -> Any:
        if not self.session:
            raise RuntimeError("HttpClient must be used as an async context manager")
        async with self.session.request(method, url, **kwargs) as response:
            return {
                "status": response.status,
                "headers": dict(response.headers),
                "text": await response.text(),
            }

    async def get(self, url: str, **kwargs) -> Any:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> Any:
        return await self.request("POST", url, **kwargs)
