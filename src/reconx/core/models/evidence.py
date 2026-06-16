import uuid
import time
from typing import Any
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    raw_output: Any
    timestamp: float = Field(default_factory=time.time)
