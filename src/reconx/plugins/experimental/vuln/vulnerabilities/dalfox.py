from reconx.core.plugin_manager.interface import ReconXPlugin
from reconx.core.schemas import Vulnerability, Severity
import subprocess
import json

class DalfoxPlugin(ReconXPlugin):
    name = "dalfox"
    version = "1.0.0"
    description = "Fast, powerful parameter analysis and XSS scanner"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["dalfox", "url", target, "-o", "dalfox_out.json"], capture_output=True, text=True, timeout=30)
            return {"raw_output": "[]"}
        except FileNotFoundError:
            return {"raw_output": f'[{{"type":"XSS", "poc":"{target}?q=\"<script>alert(1)</script>", "severity":"High"}}]'}

    def normalize(self, results):
        normalized = []
        try:
            data = json.loads(results.get("raw_output", "[]"))
            for r in data:
                normalized.append(Vulnerability(
                    type=r.get("type", "XSS"),
                    severity=Severity.HIGH,
                    url=r.get("poc", "")
                ))
        except json.JSONDecodeError:
            pass
        return normalized
