import abc
from typing import Any, Dict


class ReconXPlugin(abc.ABC):
    name: str = "unknown"
    version: str = "1.0.0"
    description: str = "Base ReconX plugin"

    def validate(self) -> bool:
        """
        Validate if the plugin can run (e.g. check dependencies).
        """
        return True

    @abc.abstractmethod
    def run(self, target: str, **kwargs) -> Dict[str, Any]:
        """
        Execute the reconnaissance tool.
        """
        pass

    def normalize(self, results: Any) -> Any:
        """
        Convert raw tool output into standard ReconX schemas.
        """
        return results
