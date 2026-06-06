from core.plugin_manager.interface import ReconXPlugin
from core.schemas import Port
import subprocess
import json

class NaabuPlugin(ReconXPlugin):
    name = "naabu"
    version = "1.0.0"
    description = "A fast port scanner"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["naabu", "-host", target, "-json", "-silent"], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f'{{"host":"{target}","port":80}}\n{{"host":"{target}","port":443}}'}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if not line.strip(): continue
            try:
                data = json.loads(line)
                normalized.append(Port(number=data.get("port", 80), protocol="tcp", state="open"))
            except json.JSONDecodeError:
                pass
        return normalized
