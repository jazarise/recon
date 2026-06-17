from pydantic import BaseModel, Field
from typing import Dict, Any


class ExecutionContext(BaseModel):
    workflow_id: str
    project_id: str = "default"
    target: str
    user: str = "system"
    variables: Dict[str, Any] = Field(default_factory=dict)
    artifacts: Dict[str, Any] = Field(default_factory=dict)

    def set_artifact(self, key: str, value: Any):
        self.artifacts[key] = value

    def get_artifact(self, key: str) -> Any:
        return self.artifacts.get(key)
