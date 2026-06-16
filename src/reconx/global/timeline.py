import datetime
import logging

logger = logging.getLogger("reconx")

class TimelineEngine:
    def __init__(self):
        # Simulated State memory { "api.example.com": ["Port 80 Open"] }
        self.history = {}

    def detect_changes(self, target: str, new_state: list) -> list:
        diffs = []
        old_state = self.history.get(target, [])
        
        # New assets appearing
        for item in new_state:
            if item not in old_state:
                diffs.append({"time": datetime.datetime.utcnow().isoformat(), "event": f"New endpoint detected: {item}"})
        
        # Assets disappearing
        for item in old_state:
            if item not in new_state:
                diffs.append({"time": datetime.datetime.utcnow().isoformat(), "event": f"Endpoint closed: {item}"})
                
        self.history[target] = new_state
        if diffs:
            logger.warning(f"[TIMELINE] Change Detected on {target}: {diffs}")
        return diffs
