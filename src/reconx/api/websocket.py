import asyncio
import logging

logger = logging.getLogger("reconx")

class StreamEngine:
    def __init__(self):
        self.connections = {}

    async def broadcast_to_tenant(self, tenant_id: str, message: str):
        if tenant_id in self.connections:
            # Simulate WebSocket write
            logger.info(f"[WSS] -> [TENANT {tenant_id}] {message}")
            await asyncio.sleep(0.1)

streamer = StreamEngine()
