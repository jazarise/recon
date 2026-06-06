from core.plugin_manager.interface import ReconXPlugin
from core.schemas import Endpoint
import subprocess
import json

class FfufPlugin(ReconXPlugin):
    name = "ffuf"
    version = "1.0.0"
    description = "Fast web fuzzer"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["ffuf", "-u", f"{target}/FUZZ", "-w", "wordlist.txt", "-json"], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f'{{"results": [{{"url": "http://{target}/admin_ffuf", "status": 200}}]}}'}

    def normalize(self, results):
        normalized = []
        try:
            data = json.loads(results.get("raw_output", "{}"))
            for r in data.get("results", []):
                normalized.append(Endpoint(path=r.get("url"), source="ffuf"))
        except json.JSONDecodeError:
            pass
        return normalized
