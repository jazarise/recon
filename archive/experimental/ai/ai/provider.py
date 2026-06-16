from abc import ABC, abstractmethod
from typing import Dict, Any

class AIProvider(ABC):
    @abstractmethod
    def analyze(self, data: Dict[str, Any]) -> str:
        pass

class MockAIProvider(AIProvider):
    def analyze(self, data: Dict[str, Any]) -> str:
        # Strictly read-only analysis mock
        return "AI Analysis complete. No exploitation performed."
