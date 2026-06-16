import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Scan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow: str
    target: str
    status: str
    started_at: float
    finished_at: Optional[float] = None
