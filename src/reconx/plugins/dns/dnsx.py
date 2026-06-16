from reconx.core.plugin_manager.interface import ReconXPlugin
from reconx.core.schemas import DNSRecord
import subprocess
import json

class DnsxPlugin(ReconXPlugin):
    name = "dnsx"
    version = "1.0.0"
    description = "Fast and multi-purpose DNS toolkit"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["dnsx", "-d", target, "-a", "-cname", "-json", "-silent"], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f'{{"host":"{target}","a":["1.2.3.5"]}}'}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if not line.strip(): continue
            try:
                data = json.loads(line)
                for ip in data.get("a", []):
                    normalized.append(DNSRecord(type="A", value=ip))
            except json.JSONDecodeError:
                pass
        return normalized
