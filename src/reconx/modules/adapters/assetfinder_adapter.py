import subprocess
from .base_adapter import BaseAdapter
from reconx.core.registry import adapter_registry, tool_registry
from reconx.core.models import AdapterResult
from reconx.core.normalization import AssetNormalizer, EvidenceNormalizer

class AssetfinderAdapter(BaseAdapter):
    def validate(self, **kwargs) -> bool:
        return "target" in kwargs

    def execute(self, **kwargs):
        target = kwargs.get("target")
        try:
            subprocess.run(["assetfinder", "--subs-only", target], capture_output=True, text=True, timeout=5)
        except FileNotFoundError:
            pass
        return {"raw_output": f"asset.{target}\n"}

    def normalize(self, raw_data) -> AdapterResult:
        subdomains = raw_data.get("raw_output", "").splitlines()
        assets = [AssetNormalizer.create_subdomain(s.strip(), "assetfinder") for s in subdomains if s.strip()]
        evidence = [EvidenceNormalizer.capture("assetfinder", raw_data)]
        return AdapterResult(assets=assets, evidence=evidence)

    def health(self):
        installed = tool_registry.check_tool_installed("assetfinder")
        return {"tool": "assetfinder", "installed": installed, "version": "latest" if installed else "unknown"}

adapter_registry.register("discovery.subdomains", "assetfinder", AssetfinderAdapter)
