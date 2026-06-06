from abc import ABC, abstractmethod
from typing import Dict, Any
from core.models import AdapterResult

class BaseAdapter(ABC):
    
    @abstractmethod
    def validate(self, **kwargs) -> bool:
        """Validate if the adapter can run with given parameters."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the underlying tool and return raw data."""
        pass

    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> AdapterResult:
        """Normalize the tool's raw output into standard AdapterResult format."""
        pass

    @abstractmethod
    def health(self) -> Dict[str, Any]:
        """Check health status of the underlying tool."""
        pass
