import uuid
from typing import List
from pydantic import BaseModel, Field

class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    scope: List[str] = []
