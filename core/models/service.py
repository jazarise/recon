from dataclasses import dataclass
from typing import Optional

@dataclass
class Service:
    host: str
    port: int
    service: str
    version: Optional[str] = None
    banner: Optional[str] = None
    protocol: str = "tcp"
