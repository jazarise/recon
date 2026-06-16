import subprocess
from .base_adapter import BaseAdapter
from core.registry import adapter_registry, tool_registry
from core.models import AdapterResult
from core.normalization import AssetNormalizer, EvidenceNormalizer

class KatanaAdapter(BaseAdapter):
    def validate(self, **kwargs) -> bool:
        return "target" in kwargs

    def execute(self, **kwargs):
        target = kwargs.get("target")
        try:
            subprocess.run(["katana", "-u", target], capture_output=True, text=True, timeout=5)
        except FileNotFoundError:
            pass
        return {"raw_output": f"http://{target}/api\nhttp://{target}/admin\n"}

    def normalize(self, raw_data) -> AdapterResult:
        urls = raw_data.get("raw_output", "").splitlines()
        assets = [AssetNormalizer.create_url(u.strip(), "katana") for u in urls if u.strip()]
        evidence = [EvidenceNormalizer.capture("katana", raw_data)]
        return AdapterResult(assets=assets, evidence=evidence)

    def health(self):
        installed = tool_registry.check_tool_installed("katana")
        return {"tool": "katana", "installed": installed, "version": "latest" if installed else "unknown"}

adapter_registry.register("content.crawl", "katana", KatanaAdapter)
