import enum
from pydantic import BaseModel, Field
from typing import List, Optional
import datetime


class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    CANCELLED = "CANCELLED"


class Task(BaseModel):
    id: str
    plugin: str
    status: TaskStatus = TaskStatus.PENDING
    depends_on: List[str] = Field(default_factory=list)
    timeout: int = 300
    retries: int = 3
    started_at: Optional[datetime.datetime] = None
    finished_at: Optional[datetime.datetime] = None
    error: Optional[str] = None
