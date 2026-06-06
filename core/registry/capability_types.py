from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class CapabilityCategory(str, Enum):
    DISCOVERY = "DISCOVERY"
    DNS = "DNS"
    ASN = "ASN"
    WEB = "WEB"
    CONTENT = "CONTENT"
    SCREENSHOT = "SCREENSHOT"
    OSINT = "OSINT"
    CLOUD = "CLOUD"
    VULNERABILITY = "VULNERABILITY"
    CORRELATION = "CORRELATION"
    REPORTING = "REPORTING"
    AI = "AI"
    ASM = "ASM"

class Priority(str, Enum):
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"

class SelectionStrategy(str, Enum):
    FASTEST = "FASTEST"
    MOST_ACCURATE = "MOST_ACCURATE"
    ALL = "ALL"

class Capability(BaseModel):
    name: str
    category: CapabilityCategory
    description: str
    adapters: List[str] = []
    priority: Priority = Priority.NORMAL
