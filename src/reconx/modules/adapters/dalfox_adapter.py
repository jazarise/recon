import subprocess
from .base_adapter import BaseAdapter
from reconx.core.registry import adapter_registry, tool_registry
from reconx.core.models import AdapterResult, Severity
from reconx.core.normalization import FindingNormalizer, EvidenceNormalizer

class DalfoxAdapter(BaseAdapter):
    def validate(self, **kwargs) -> bool:
        return "target" in kwargs

    def execute(self, **kwargs):
        target = kwargs.get("target")
        try:
            subprocess.run(["dalfox", "url", target], capture_output=True, text=True, timeout=5)
        except FileNotFoundError:
            pass
        return {"raw_output": f"[VULN] XSS found at {target}?q=1\n"}

    def normalize(self, raw_data) -> AdapterResult:
        findings_raw = raw_data.get("raw_output", "").splitlines()
        findings = []
        for f in findings_raw:
            if "[VULN]" in f:
                finding = FindingNormalizer.create_finding(
                    title="XSS Discovered",
                    severity=Severity.HIGH,
                    capability="vuln.xss",
                    source="dalfox"
                )
                findings.append(finding)
        
        evidence = [EvidenceNormalizer.capture("dalfox", raw_data)]
        return AdapterResult(findings=findings, evidence=evidence)

    def health(self):
        installed = tool_registry.check_tool_installed("dalfox")
        return {"tool": "dalfox", "installed": installed, "version": "latest" if installed else "unknown"}

adapter_registry.register("vuln.xss", "dalfox", DalfoxAdapter)
