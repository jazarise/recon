from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any, Dict
from abc import ABC, abstractmethod

class FindingData(BaseModel):
    tool: str
    target: str
    severity: str
    finding_type: str
    data: Dict[str, Any]
    raw_output: str
    timestamp: str
    
    model_config = ConfigDict(extra="ignore")

class ReconXPlugin(ABC):
    name: str = ""
    version: str = "1.0.0"
    capabilities: List[str] = []

    @abstractmethod
    async def validate(self) -> bool:
        """Validate if the plugin can run (e.g. check if binary exists)."""
        pass

    @abstractmethod
    async def execute(self, target: str, **kwargs) -> List[FindingData]:
        """Execute the plugin against a target and return structured findings."""
        pass
