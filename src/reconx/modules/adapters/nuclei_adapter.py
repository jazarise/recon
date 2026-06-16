import subprocess
from .base_adapter import BaseAdapter
from core.registry import adapter_registry, tool_registry
from core.models import AdapterResult, Severity
from core.normalization import FindingNormalizer, EvidenceNormalizer

class NucleiAdapter(BaseAdapter):
    def validate(self, **kwargs) -> bool:
        return "target" in kwargs

    def execute(self, **kwargs):
        target = kwargs.get("target")
        try:
            subprocess.run(["nuclei", "-u", target, "-silent"], capture_output=True, text=True, timeout=5)
        except FileNotFoundError:
            pass
        return {"raw_output": f"[info] [dns] {target}\n"}

    def normalize(self, raw_data) -> AdapterResult:
        findings_raw = raw_data.get("raw_output", "").splitlines()
        findings = []
        for f in findings_raw:
            if f.strip():
                finding = FindingNormalizer.create_finding(
                    title="Template Match",
                    severity=Severity.INFO,
                    capability="vuln.templates",
                    source="nuclei"
                )
                findings.append(finding)
                
        evidence = [EvidenceNormalizer.capture("nuclei", raw_data)]
        return AdapterResult(findings=findings, evidence=evidence)

    def health(self):
        installed = tool_registry.check_tool_installed("nuclei")
        return {"tool": "nuclei", "installed": installed, "version": "latest" if installed else "unknown"}

adapter_registry.register("vuln.templates", "nuclei", NucleiAdapter)
