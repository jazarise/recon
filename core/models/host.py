from dataclasses import dataclass
from typing import Optional

@dataclass
class Host:
    ip: str
    hostname: Optional[str] = None
