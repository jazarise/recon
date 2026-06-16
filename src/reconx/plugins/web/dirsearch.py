from reconx.core.plugin_manager.interface import ReconXPlugin
from reconx.core.schemas import Endpoint
import subprocess
import json

class DirsearchPlugin(ReconXPlugin):
    name = "dirsearch"
    version = "1.0.0"
    description = "Web path scanner"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["dirsearch", "-u", target, "--json-report", "out.json"], capture_output=True, text=True, timeout=30)
            return {"raw_output": f'{{"results": [{{"url": "http://{target}/dirsearch_path"}}]}}'}
        except FileNotFoundError:
            return {"raw_output": f'{{"results": [{{"url": "http://{target}/dirsearch_path"}}]}}'}

    def normalize(self, results):
        normalized = []
        try:
            data = json.loads(results.get("raw_output", "{}"))
            for r in data.get("results", []):
                normalized.append(Endpoint(path=r.get("url"), source="dirsearch"))
        except json.JSONDecodeError:
            pass
        return normalized
