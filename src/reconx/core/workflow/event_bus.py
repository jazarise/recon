from typing import Callable, Dict, List, Any
import asyncio


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    async def publish(self, event_type: str, payload: Any):
        if event_type in self._subscribers:
            callbacks = self._subscribers[event_type]
            await asyncio.gather(
                *(cb(payload) for cb in callbacks if asyncio.iscoroutinefunction(cb))
            )


event_bus = EventBus()
