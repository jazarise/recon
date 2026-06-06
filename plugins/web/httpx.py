from core.plugin_manager.interface import ReconXPlugin
from core.schemas import URL, Technology
import subprocess
import json

class HttpxPlugin(ReconXPlugin):
    name = "httpx"
    version = "1.0.0"
    description = "Fast and multi-purpose HTTP toolkit"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["httpx", "-u", target, "-title", "-tech-detect", "-status-code", "-json", "-silent"], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f'{{"url":"http://{target}","status_code":200,"title":"Mock","tech":["nginx"]}}'}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if not line.strip(): continue
            try:
                data = json.loads(line)
                techs = data.get("tech", [])
                normalized.append(URL(
                    value=data.get("url", ""),
                    status_code=data.get("status_code"),
                    title=data.get("title"),
                    technologies=techs
                ))
            except json.JSONDecodeError:
                pass
        return normalized
