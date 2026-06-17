from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class StandardResponse(BaseModel):
    success: bool
    message: str
    data: Any = {}
    errors: List[str] = []


class ScanRequest(BaseModel):
    target: str = Field(..., example="example.com", description="The target to scan")
    workflow: str = Field(
        ..., example="passive", description="The workflow name to run"
    )
    options: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Additional options"
    )
