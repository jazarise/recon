import logging

logger = logging.getLogger("reconx")

class WebhookDispatcher:
    def __init__(self, endpoint_url: str = None):
        self.endpoint_url = endpoint_url

    def dispatch(self, event_type: str, data: dict):
        if not self.endpoint_url:
            return
            
        payload = {
            "event": event_type,
            "data": data
        }
        logger.warning(f"[WEBHOOK] Dispatched {event_type} to {self.endpoint_url}")
        # Simulated POST request logic
