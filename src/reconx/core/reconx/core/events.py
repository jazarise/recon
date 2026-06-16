import asyncio
from typing import Callable, Dict, List, Any
from core.reconx.utils.logger import logger

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to {event_type}", callback=callback.__name__)

    async def publish(self, event_type: str, **kwargs: Any):
        if event_type in self._subscribers:
            logger.debug(f"Publishing event {event_type}")
            tasks = []
            for callback in self._subscribers[event_type]:
                if asyncio.iscoroutinefunction(callback):
                    tasks.append(asyncio.create_task(callback(**kwargs)))
                else:
                    try:
                        callback(**kwargs)
                    except Exception:
                        logger.error(f"Error in sync event callback for {event_type}", exc_info=True)
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

event_bus = EventBus()
