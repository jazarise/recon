import asyncio

class QueueManager:
    def __init__(self):
        self.local_queue = asyncio.PriorityQueue()

    async def enqueue(self, item, priority=1):
        await self.local_queue.put((priority, item))

    async def dequeue(self):
        return await self.local_queue.get()
