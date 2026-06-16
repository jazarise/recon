from abc import ABC, abstractmethod
from typing import Any
from reconx.core.models import AdapterResult

class BaseNativeModule(ABC):
    """
    Standard contract for all native execution modules.
    Ensures exactly ONE canonical implementation per capability.
    """
    
    @abstractmethod
    def run(self, target: str) -> Any:
        """Executes the native logic and returns raw structures."""
        pass

    @abstractmethod
    def normalize(self, raw_data: Any) -> AdapterResult:
        """Translates the native outputs directly into the Unified Data Model."""
        pass
        
    def execute(self, target: str) -> AdapterResult:
        """Standard wrapper that runs and normalizes seamlessly."""
        raw = self.run(target)
        return self.normalize(raw)
