from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class Subdomain:
    value: str
    source: str
    confidence: str = "high"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
