import yaml
import importlib.util
import ast
from pathlib import Path
from typing import Type
from reconx.core.plugins.base import ReconXPlugin
from reconx.core.plugins.validator import validate_plugin_security, validate_metadata
from reconx.core.plugins.exceptions import PluginValidationError

PLUGINS_DIR = Path(__file__).parent.parent.parent / "plugins"

class PluginLoader:
    @staticmethod
    def is_safe_module(py_file: Path) -> bool:
        with open(py_file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(py_file))
        
        for node in tree.body:
            if not isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef, ast.FunctionDef, ast.Assign, ast.Expr)):
                return False
            # Check if Expr is just a docstring
            if isinstance(node, ast.Expr) and not isinstance(node.value, ast.Constant):
                return False
        return True

    @staticmethod
    def load_plugin(plugin_dir: Path, trusted_root: Path = PLUGINS_DIR) -> Type[ReconXPlugin]:
        # Enforce plugin root
        try:
            plugin_dir = plugin_dir.resolve(strict=True)
            plugin_root = trusted_root.resolve(strict=True)
            if not plugin_dir.is_relative_to(plugin_root):
                raise PluginValidationError("Path traversal blocked: plugin outside of trusted root.")
        except Exception as e:
            raise PluginValidationError(f"Invalid plugin path: {e}")

        yaml_file = plugin_dir / "plugin.yaml"
        py_file = plugin_dir / "plugin.py"

        if not yaml_file.exists():
            raise PluginValidationError(f"Missing plugin.yaml in {plugin_dir}")
        if not py_file.exists():
            raise PluginValidationError(f"Missing plugin.py in {plugin_dir}")

        with open(yaml_file, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)

        if not isinstance(metadata, dict):
            raise PluginValidationError("Invalid plugin.yaml format")
            
        # Manifest validation
        for field in ["name", "version", "author"]:
            if field not in metadata or not metadata[field]:
                raise PluginValidationError(f"Manifest missing required field: {field}")

        validate_metadata(metadata)
        validate_plugin_security(py_file)
        
        if not PluginLoader.is_safe_module(py_file):
            raise PluginValidationError("Plugin contains execution at module level.")

        # Load the module
        spec = importlib.util.spec_from_file_location(
            f"reconx.plugins.{metadata['name']}", py_file
        )
        if spec is None or spec.loader is None:
            raise PluginValidationError(f"Could not load python module from {py_file}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find register() entrypoint
        if not hasattr(module, "register"):
            raise PluginValidationError(f"Plugin must expose a register() entrypoint in {py_file}")
            
        plugin_class = module.register()

        if not plugin_class or not issubclass(plugin_class, ReconXPlugin):
            raise PluginValidationError(
                f"register() must return a ReconXPlugin subclass in {py_file}"
            )

        try:
            # Test instantiation to catch missing abstract methods
            _ = plugin_class()
        except TypeError as e:
            raise PluginValidationError(
                f"Plugin class {plugin_class.__name__} cannot be instantiated: {e}"
            )

        return plugin_class
