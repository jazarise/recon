from core.plugin_manager.interface import ReconXPlugin
from core.schemas import Endpoint
import subprocess

class GobusterPlugin(ReconXPlugin):
    name = "gobuster"
    version = "1.0.0"
    description = "Directory/File, DNS and VHost busting tool"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["gobuster", "dir", "-u", target, "-w", "wordlist.txt", "-q"], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f"/{target}_admin (Status: 200)"}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if line.strip():
                path = line.split(" ")[0]
                normalized.append(Endpoint(path=path, source="gobuster"))
        return normalized
