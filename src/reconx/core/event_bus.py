from typing import Callable, Dict, List, Any
from collections import defaultdict
from core.logger import logger

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, callback: Callable):
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to {event_type}")

    def emit(self, event_type: str, **kwargs: Any):
        logger.info(f"Event: {event_type} | {kwargs}")
        for callback in self.subscribers.get(event_type, []):
            try:
                callback(**kwargs)
            except Exception as e:
                logger.error(f"Error in event subscriber for {event_type}: {e}")

event_bus = EventBus()
