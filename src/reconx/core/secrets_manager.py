import os
from pathlib import Path
from typing import Dict

from reconx.core.paths import BASE_DIR

class SecretsManager:
    """Manages secure injection of secrets into plugin environments."""
    
    def __init__(self):
        self._secrets = {}
        # Load from .env file if present
        env_file = BASE_DIR / ".env"
        if env_file.exists():
            self._load_env_file(env_file)
        # Fallback to OS environment
        for key in ["SHODAN_API_KEY", "VIRUSTOTAL_API_KEY", "GITHUB_TOKEN", "OPENAI_API_KEY"]:
            if key not in self._secrets and os.environ.get(key):
                self._secrets[key] = os.environ[key]

    def _load_env_file(self, path: Path):
        try:
            if os.name != "nt":
                os.chmod(path, 0o600)
        except Exception:
            pass
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    self._secrets[key.strip()] = value.strip()

    def get_plugin_environment(self, plugin_name: str) -> Dict[str, str]:
        """
        Returns a dictionary of environment variables safely scoped for a plugin.
        """
        env = {
            "PATH": os.environ.get("PATH", ""),
            "PYTHONPATH": str(BASE_DIR),
            "RECONX_PLUGIN": plugin_name,
            "HOME": os.environ.get("HOME", os.environ.get("USERPROFILE", "")),
        }
        
        # Linux: preserve critical vars
        for var in ["LANG", "LC_ALL", "TERM"]:
            val = os.environ.get(var)
            if val:
                env[var] = val
        
        # Windows: preserve SYSTEMROOT if present
        sr = os.environ.get("SYSTEMROOT")
        if sr:
            env["SYSTEMROOT"] = sr
        
        # Inject specific secrets based on plugin name
        plugin_secret_map = {
            "network_discovery": ["SHODAN_API_KEY"],
            "web_recon": ["VIRUSTOTAL_API_KEY"],
            "llm_analysis": ["OPENAI_API_KEY"],
        }
        
        for key in plugin_secret_map.get(plugin_name, []):
            if key in self._secrets:
                env[key] = self._secrets[key]
            
        return env
