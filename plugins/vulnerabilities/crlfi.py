from core.plugin_manager.interface import ReconXPlugin
from core.schemas import Vulnerability, Severity
import subprocess
import json

class CrlfiPlugin(ReconXPlugin):
    name = "crlfi"
    version = "1.0.0"
    description = "CRLF Injection scanner"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["crlfi", "-u", target], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f"[VULN] CRLF found at {target}/%0d%0a"}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if "[VULN]" in line:
                normalized.append(Vulnerability(
                    type="CRLF_Injection",
                    severity=Severity.MEDIUM,
                    url=line.split()[-1]
                ))
        return normalized
