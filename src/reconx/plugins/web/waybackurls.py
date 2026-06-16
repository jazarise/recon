from reconx.core.plugin_manager.interface import ReconXPlugin
from reconx.core.schemas import Endpoint
import subprocess

class WaybackurlsPlugin(ReconXPlugin):
    name = "waybackurls"
    version = "1.0.0"
    description = "Fetch all the URLs that the Wayback Machine knows about for a domain"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["waybackurls", target], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f"http://{target}/old_path"}

    def normalize(self, results):
        return [Endpoint(path=line.strip(), source="waybackurls") for line in results.get("raw_output", "").splitlines() if line.strip()]
