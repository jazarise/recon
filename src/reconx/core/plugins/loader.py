import yaml
import importlib.util
from pathlib import Path
from typing import Type
from reconx.core.plugins.base import ReconXPlugin
from reconx.core.plugins.validator import validate_plugin_security, validate_metadata
from reconx.core.plugins.exceptions import PluginValidationError


class PluginLoader:
    @staticmethod
    def load_plugin(plugin_dir: Path) -> Type[ReconXPlugin]:
        yaml_file = plugin_dir / "plugin.yaml"
        py_file = plugin_dir / "plugin.py"

        if not yaml_file.exists():
            raise PluginValidationError(f"Missing plugin.yaml in {plugin_dir}")
        if not py_file.exists():
            raise PluginValidationError(f"Missing plugin.py in {plugin_dir}")

        with open(yaml_file, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)

        validate_metadata(metadata)
        validate_plugin_security(py_file)

        # Load the module
        spec = importlib.util.spec_from_file_location(
            f"reconx.plugins.{metadata['name']}", py_file
        )
        if spec is None or spec.loader is None:
            raise PluginValidationError(f"Could not load python module from {py_file}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find the ReconXPlugin class
        plugin_class = None
        for item_name in dir(module):
            item = getattr(module, item_name)
            if (
                isinstance(item, type)
                and issubclass(item, ReconXPlugin)
                and item is not ReconXPlugin
            ):
                plugin_class = item
                break

        if not plugin_class:
            raise PluginValidationError(
                f"No class inheriting from ReconXPlugin found in {py_file}"
            )

        try:
            # Test instantiation to catch missing abstract methods
            _ = plugin_class()
        except TypeError as e:
            raise PluginValidationError(
                f"Plugin class {plugin_class.__name__} cannot be instantiated: {e}"
            )

        return plugin_class
