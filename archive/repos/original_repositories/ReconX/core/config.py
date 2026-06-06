import yaml
import os
from pathlib import Path
from core.paths import PROJECT_ROOT

class ConfigManager:
    """Central configuration manager for ReconX."""
    _instance = None
    _config = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = PROJECT_ROOT / "config.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f) or {}

    def get(self, key_path: str, default=None):
        """Get a configuration value using dot notation (e.g., 'general.threads')."""
        keys = key_path.split('.')
        val = self._config
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val

# Global instance for easy access
config = ConfigManager()
