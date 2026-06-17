import abc
from typing import Any, Dict, List


class ReconXPlugin(abc.ABC):
    """
    Base class for all ReconX Plugins.
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The unique name of the plugin."""
        pass

    @property
    @abc.abstractmethod
    def version(self) -> str:
        """The version of the plugin."""
        pass

    @abc.abstractmethod
    async def execute(self, target: str, **kwargs) -> Any:
        """
        Execute the tool against the target.
        """
        pass

    @abc.abstractmethod
    def parse(self, output: Any) -> List[Dict[str, Any]]:
        """
        Parse the raw output into a list of normalized Asset/Finding dictionaries.
        """
        pass
