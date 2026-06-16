from core.plugin_manager.interface import ReconXPlugin
from core.schemas import Endpoint
import subprocess

class HakrawlerPlugin(ReconXPlugin):
    name = "hakrawler"
    version = "1.0.0"
    description = "Fast, plain-text web crawler"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["hakrawler", "-url", target], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f"http://{target}/hakrawler_found"}

    def normalize(self, results):
        return [Endpoint(path=line.strip(), source="hakrawler") for line in results.get("raw_output", "").splitlines() if line.strip()]
