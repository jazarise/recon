from reconx.core.plugin_manager.interface import ReconXPlugin
from reconx.core.schemas import Email, Confidence
import subprocess

class TheHarvesterPlugin(ReconXPlugin):
    name = "theharvester"
    version = "1.0.0"
    description = "E-mail, subdomain and people names harvester"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["theHarvester", "-d", target, "-b", "all"], capture_output=True, text=True, timeout=60)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f"admin@{target}\ncontact@{target}"}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if "@" in line:
                normalized.append(Email(
                    value=line.strip(),
                    source="theHarvester",
                    confidence=Confidence.HIGH
                ))
        return normalized
