from datetime import datetime
from collections import defaultdict
from typing import List, Dict


class TimelineEngine:
    def __init__(self):
        # target -> timeline of events
        self.ledgers: Dict[str, List[dict]] = defaultdict(list)

    def log_change(self, target: str, event_type: str, details: str):
        """Records a chronological ledger entry."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "details": details,
        }
        self.ledgers[target].append(entry)
        print(f"[TIMELINE] {target}: {event_type} - {details}")

    def get_timeline(self, target: str) -> List[dict]:
        return self.ledgers.get(target, [])

    def get_all_ledgers(self) -> Dict[str, List[dict]]:
        return dict(self.ledgers)


timeline_engine = TimelineEngine()
