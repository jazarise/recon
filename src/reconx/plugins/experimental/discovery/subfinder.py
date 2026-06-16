from reconx.core.plugin_manager.interface import ReconXPlugin
from reconx.core.schemas import Domain
import subprocess
import json

class SubfinderPlugin(ReconXPlugin):
    name = "subfinder"
    version = "1.0.0"
    description = "Fast passive subdomain enumeration tool"

    def run(self, target: str, **kwargs):
        # Mock execution or actual execution if binary exists
        try:
            result = subprocess.run(["subfinder", "-d", target, "-silent", "-json"], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            # Mock if not installed
            return {"raw_output": f'{{"host":"sub1.{target}","source":"mock"}}\n{{"host":"sub2.{target}","source":"mock"}}'}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if not line.strip(): continue
            try:
                data = json.loads(line)
                normalized.append(Domain(value=data.get("host", ""), source="subfinder"))
            except json.JSONDecodeError:
                pass
        return normalized
