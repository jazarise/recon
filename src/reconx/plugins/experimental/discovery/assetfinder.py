from reconx.core.plugin_manager.interface import ReconXPlugin
from reconx.core.schemas import Domain
import subprocess

class AssetfinderPlugin(ReconXPlugin):
    name = "assetfinder"
    version = "1.0.0"
    description = "Find domains and subdomains related to a given domain"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["assetfinder", "--subs-only", target], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f'af-sub.{target}\n'}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if line.strip():
                normalized.append(Domain(value=line.strip(), source="assetfinder"))
        return normalized
