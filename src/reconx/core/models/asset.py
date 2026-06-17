import uuid
from typing import List
from pydantic import BaseModel, Field
from .enums import AssetType

class Asset(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: AssetType
    value: str
    source: str = "unknown"
    confidence: float = 1.0
    tags: List[str] = []
