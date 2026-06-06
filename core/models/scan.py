from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
from .finding import Finding

@dataclass
class Scan:
    target: str
    workflow: str
    status: str = "running"
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    duration: Optional[float] = None
    plugins_used: List[str] = field(default_factory=list)
    findings: List[Finding] = field(default_factory=list)
