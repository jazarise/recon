import asyncio
import logging

logger = logging.getLogger("reconx")

class EventBus:
    def __init__(self):
        self.subscribers = {}
        self.queue = asyncio.Queue()

    def subscribe(self, event_type: str, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    async def publish(self, event_type: str, data: dict):
        logger.debug(f"EventBus Emitting: {event_type}")
        await self.queue.put((event_type, data))

    async def process_events(self):
        while True:
            event_type, data = await self.queue.get()
            if event_type in self.subscribers:
                for callback in self.subscribers[event_type]:
                    asyncio.create_task(callback(data))
            self.queue.task_done()
