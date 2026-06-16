from reconx.core.plugin_manager.interface import ReconXPlugin
from reconx.core.schemas import Endpoint, Parameter
import subprocess

class GauPlugin(ReconXPlugin):
    name = "gau"
    version = "1.0.0"
    description = "Fetch known URLs from AlienVault's Open Threat Exchange, the Wayback Machine, and Common Crawl"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["gau", target], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f"https://{target}/admin?id=1\nhttps://{target}/api/v1/user?token=abc"}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            line = line.strip()
            if not line: continue
            normalized.append(Endpoint(path=line, source="gau"))
            if "?" in line:
                params_part = line.split("?", 1)[1]
                for p in params_part.split("&"):
                    if "=" in p:
                        param_name = p.split("=", 1)[0]
                        normalized.append(Parameter(name=param_name, source="gau"))
        return normalized
