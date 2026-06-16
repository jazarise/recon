from reconx.core.plugin_manager.interface import ReconXPlugin
from reconx.core.schemas import ThreatIndicator, Confidence

class ThreatIntelPlugin(ReconXPlugin):
    name = "threat_intel"
    version = "1.0.0"
    description = "Threat intelligence aggregator"

    def run(self, target: str, **kwargs):
        return {"raw_output": f"{target} -> Malicious IP 1.2.3.4"}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if "Malicious IP" in line:
                ip = line.split(" ")[-1]
                normalized.append(ThreatIndicator(
                    indicator_type="ip",
                    value=ip,
                    source="threat_intel",
                    confidence=Confidence.MEDIUM
                ))
        return normalized
