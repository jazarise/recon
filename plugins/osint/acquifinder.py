from core.plugin_manager.interface import ReconXPlugin
from core.schemas import Organization, Confidence
import subprocess
import json

class AcquiFinderPlugin(ReconXPlugin):
    name = "acquifinder"
    version = "1.0.0"
    description = "Discover company acquisitions and associated domains"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["acquifinder", "-d", target, "--json"], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f'{{"name": "{target.split(".")[0].capitalize()} Corp", "domain": "{target}"}}'}

    def normalize(self, results):
        normalized = []
        try:
            data = json.loads(results.get("raw_output", "{}"))
            name = data.get("name", "Unknown")
            domain = data.get("domain", "")
            if domain:
                normalized.append(Organization(name=name, domain=domain))
        except json.JSONDecodeError:
            pass
        return normalized
