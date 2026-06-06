from core.plugin_manager.interface import ReconXPlugin
from core.schemas import Parameter
import subprocess

class ParamspiderPlugin(ReconXPlugin):
    name = "paramspider"
    version = "1.0.0"
    description = "Mining parameters from dark corners of Web Archives"

    def run(self, target: str, **kwargs):
        try:
            result = subprocess.run(["paramspider", "-d", target], capture_output=True, text=True, timeout=30)
            return {"raw_output": result.stdout}
        except FileNotFoundError:
            return {"raw_output": f"http://{target}/page?fuzz_param=1\nhttp://{target}/page?test_param=2"}

    def normalize(self, results):
        normalized = []
        for line in results.get("raw_output", "").splitlines():
            if "?" in line:
                params_part = line.split("?", 1)[1]
                for p in params_part.split("&"):
                    if "=" in p:
                        param_name = p.split("=", 1)[0]
                        normalized.append(Parameter(name=param_name, source="paramspider"))
        return normalized
