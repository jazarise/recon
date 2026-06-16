from core.paths import BASE_DIR

import yaml
import os
import threading


class ConfigManager:
    """Central configuration manager for ReconX."""
    _instance = None
    _config = {}
    _lock = threading.Lock()

    # Default values
    DEFAULTS = {
        "workspace": str(BASE_DIR / "workspace"),
        "reports": str(BASE_DIR / "reports"),
        "concurrency": 20,
        "timeout": 30,
        "general": {
            "threads": 10,
            "log_level": "INFO"
        },
        "dashboard": {
            "host": "127.0.0.1",
            "port": 8000
        }
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = BASE_DIR / "config.yaml"
        with self._lock:
            # 1. Load defaults
            self._config = self._merge_dicts({}, self.DEFAULTS)
            
            # 2. Merge config.yaml if exists
            if config_path.exists():
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        file_config = yaml.safe_load(f) or {}
                        self._config = self._merge_dicts(self._config, file_config)
                except Exception as e:
                    # If logging isn't set up yet, fallback to print
                    print(f"Warning: Failed to load config.yaml: {e}")
                    
            # 3. Environment variables (RECONX_*)
            self._apply_env_vars(self._config)

    def _merge_dicts(self, d1: dict, d2: dict) -> dict:
        merged = d1.copy()
        for k, v in d2.items():
            if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
                merged[k] = self._merge_dicts(merged[k], v)
            else:
                merged[k] = v
        return merged

    def _apply_env_vars(self, config_dict: dict, prefix: str = "RECONX_"):
        """Override configuration with environment variables."""
        for key, value in os.environ.items():
            if key.startswith(prefix):
                # e.g., RECONX_GENERAL_THREADS -> general.threads
                clean_key = key[len(prefix):].lower()
                parts = clean_key.split('_')
                self._set_nested_val(config_dict, parts, value)

    def _set_nested_val(self, d: dict, keys: list, value: str):
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        # Type casting based on existing default if possible
        existing = d.get(keys[-1])
        if isinstance(existing, int):
            try:
                value = int(value)
            except ValueError:
                pass
        elif isinstance(existing, bool):
            value = str(value).lower() in ("true", "1", "yes")
        d[keys[-1]] = value

    def get(self, key_path: str, default=None):
        """Get a configuration value using dot notation (e.g., 'general.threads')."""
        keys = key_path.split('.')
        with self._lock:
            val = self._config
            for k in keys:
                if isinstance(val, dict) and k in val:
                    val = val[k]
                else:
                    return default
            return val

    def set(self, key_path: str, value):
        """Set runtime overrides."""
        keys = key_path.split('.')
        with self._lock:
            d = self._config
            for k in keys[:-1]:
                d = d.setdefault(k, {})
            d[keys[-1]] = value

# Global instance for easy access
config = ConfigManager()
