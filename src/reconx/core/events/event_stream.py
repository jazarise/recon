import asyncio
import json
from typing import Callable, List, Any


class EventStream:
    """A simple Pub/Sub event bus for live recon monitoring."""

    def __init__(self):
        self.subscribers: List[Callable[[str], Any]] = []

    def subscribe(self, callback: Callable[[str], Any]):
        self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[str], Any]):
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    async def emit(self, event_type: str, data: dict):
        """Emits an event to all connected subscribers asynchronously."""
        payload = json.dumps({"event": event_type, "data": data})
        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(payload)
                else:
                    callback(payload)
            except Exception as e:
                print(f"[-] EventStream error: {e}")

    def sync_emit(self, event_type: str, data: dict):
        """Emits an event synchronously by scheduling it on the running loop or running it."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.emit(event_type, data))
        except RuntimeError:
            # If no running loop, just run it
            asyncio.run(self.emit(event_type, data))


event_stream = EventStream()
