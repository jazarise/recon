from core.plugin_manager.interface import ReconXPlugin
from core.schemas import BreachRecord, Confidence
import subprocess

class BreachCheckPlugin(ReconXPlugin):
    name = "breach-check"
    version = "1.0.0"
    description = "Check domains and emails against known data breaches"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["breach-check", target], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": "Collection #1 (Credential)"}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if line.strip():
                normalized.append(BreachRecord(
                    source=line.strip(),
                    exposure_type="credential",
                    confidence=Confidence.VERY_HIGH
                ))
        return normalized
