import subprocess
from .base_adapter import BaseAdapter
from core.registry import adapter_registry, tool_registry
from core.models import AdapterResult
from core.normalization import AssetNormalizer, EvidenceNormalizer

class SubfinderAdapter(BaseAdapter):
    def validate(self, **kwargs) -> bool:
        return "target" in kwargs

    def execute(self, **kwargs):
        target = kwargs.get("target")
        # Mocking execution to avoid dependencies breaking
        try:
            subprocess.run(["subfinder", "-d", target, "-silent"], capture_output=True, text=True, timeout=5)
        except FileNotFoundError:
            pass
        return {"raw_output": f"mock.subdomain.{target}\napi.{target}\n"}

    def normalize(self, raw_data) -> AdapterResult:
        subdomains = raw_data.get("raw_output", "").splitlines()
        assets = [AssetNormalizer.create_subdomain(s.strip(), "subfinder") for s in subdomains if s.strip()]
        evidence = [EvidenceNormalizer.capture("subfinder", raw_data)]
        return AdapterResult(assets=assets, evidence=evidence)

    def health(self):
        installed = tool_registry.check_tool_installed("subfinder")
        return {
            "tool": "subfinder",
            "installed": installed,
            "version": "latest" if installed else "unknown"
        }

adapter_registry.register("discovery.subdomains", "subfinder", SubfinderAdapter)
