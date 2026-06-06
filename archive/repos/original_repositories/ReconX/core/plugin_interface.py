import abc

class PluginInterface(abc.ABC):
    @abc.abstractmethod
    async def execute(self, config: dict, context: dict) -> dict:
        """
        Execute the plugin.
        
        Args:
            config: Plugin-specific configuration.
            context: Global context including the target and previous steps' outputs.
            
        Returns:
            dict: Structured output including standard fields like plugin name, status, etc.
        """
        pass
