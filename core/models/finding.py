from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Finding:
    category: str
    value: str
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
