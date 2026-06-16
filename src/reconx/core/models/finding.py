import uuid
from typing import Optional
from pydantic import BaseModel, Field
from .enums import Severity

class Finding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    severity: Severity
    asset_id: Optional[str] = None
    capability: str
    source: str = "unknown"
