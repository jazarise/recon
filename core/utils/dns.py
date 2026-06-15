import asyncio
import socket

class DnsResolver:
    @staticmethod
    async def resolve_a(hostname: str) -> list:
        loop = asyncio.get_running_loop()
        try:
            # simple async dns wrapper
            ips = await loop.run_in_executor(None, socket.gethostbyname_ex, hostname)
            return ips[2] if len(ips) > 2 else []
        except Exception:
            return []
