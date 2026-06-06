import importlib
import pkgutil
import inspect
from typing import Dict, Type
from reconx.utils.logger import logger
from reconx.plugins.base import ReconXPlugin
import reconx.integrations

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, Type[ReconXPlugin]] = {}

    def load_plugins(self, package=reconx.integrations):
        """Dynamically load all plugins in the given package."""
        logger.info(f"Loading plugins from {package.__name__}")
        
        for _, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            try:
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, ReconXPlugin) and obj != ReconXPlugin:
                        self.plugins[obj.name] = obj
                        logger.debug(f"Loaded plugin: {obj.name} v{obj.version}")
            except Exception as e:
                logger.error(f"Failed to load module {module_name}", exc_info=e)
                
        return self.plugins
