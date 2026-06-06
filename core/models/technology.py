from dataclasses import dataclass
from typing import Optional

@dataclass
class Technology:
    host: str
    name: str
    version: Optional[str] = None
