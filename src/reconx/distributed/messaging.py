import asyncio
import logging

logger = logging.getLogger("reconx")

class MessageBroker:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageBroker, cls).__new__(cls)
            cls._instance.subscribers = {}
            cls._instance.queue = asyncio.Queue()
        return cls._instance

    def subscribe(self, event_type: str, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    async def publish(self, event_type: str, data: dict):
        logger.debug(f"[BROKER] Emitting: {event_type}")
        await self.queue.put((event_type, data))

    async def run_listener(self):
        while True:
            event_type, data = await self.queue.get()
            if event_type in self.subscribers:
                for callback in self.subscribers[event_type]:
                    asyncio.create_task(callback(data))
            self.queue.task_done()
