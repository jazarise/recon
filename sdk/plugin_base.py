from typing import List, Any
from core.models.finding import Finding
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """
    The strict standard interface for any ReconX ecosystem plugin.
    All plugins must inherit from this class and return a List[Finding].
    """
    
    name: str = "BasePlugin"
    version: str = "1.0.0"
    
    @abstractmethod
    async def execute(self, target: str, **kwargs) -> List[Finding]:
        """
        Execute the plugin against a target and yield findings.
        """
        pass
