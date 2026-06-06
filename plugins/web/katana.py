from core.plugin_manager.interface import ReconXPlugin
from core.schemas import URL
import subprocess
import json

class KatanaPlugin(ReconXPlugin):
    name = "katana"
    version = "1.0.0"
    description = "A next-generation crawling and spidering framework"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["katana", "-u", target, "-json", "-silent"], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f'{{"endpoint":"http://{target}/api/v1"}}'}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if not line.strip(): continue
            try:
                data = json.loads(line)
                normalized.append(URL(value=data.get("endpoint", "")))
            except json.JSONDecodeError:
                pass
        return normalized
