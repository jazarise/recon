import os
from pathlib import Path

BASE_DIR = Path("e:/ReconX/Reconx_V_2.0.0")

FILES = {
    "core/engine/correlation_engine.py": """from core.schemas import HostProfile, Domain, IPAddress, Port, URL, Technology, DNSRecord, Endpoint, Parameter, Vulnerability, Finding
from typing import List, Any

class CorrelationEngine:
    def __init__(self):
        self.hosts = {}

    def ingest(self, results: List[Any]):
        for item in results:
            if isinstance(item, Domain):
                if item.value not in self.hosts:
                    self.hosts[item.value] = HostProfile(domain=item.value)
            elif isinstance(item, IPAddress):
                # For simplicity, assuming global map
                pass
            elif isinstance(item, Port):
                for h in self.hosts.values():
                    if item.number not in h.ports:
                        h.ports.append(item.number)
            elif isinstance(item, URL):
                for h in self.hosts.values():
                    if item.value not in h.urls:
                        h.urls.append(item.value)
                    h.technologies.extend(item.technologies)
            elif isinstance(item, DNSRecord):
                for h in self.hosts.values():
                    h.dns_records.append(item)
            elif isinstance(item, Endpoint):
                for h in self.hosts.values():
                    h.endpoints.append(item)
            elif isinstance(item, Parameter):
                for h in self.hosts.values():
                    h.parameters.append(item)
            elif isinstance(item, Vulnerability):
                for h in self.hosts.values():
                    h.vulnerabilities.append(item)
            elif isinstance(item, Finding):
                for h in self.hosts.values():
                    h.findings.append(item)

    def get_profiles(self) -> List[HostProfile]:
        return list(self.hosts.values())
""",
    "workflows/webassess.yaml": """name: Web Security Assessment Workflow
description: Discovery through parameter mining and vulnerability checks
steps:
  - name: Subdomain Enumeration
    plugin: subfinder
  - name: DNS Intelligence
    plugin: dnsx
  - name: Port Scanning
    plugin: naabu
  - name: HTTP Analysis
    plugin: httpx
  - name: Endpoint Discovery
    plugin: gau
  - name: Parameter Discovery
    plugin: paramspider
  - name: Vulnerability Checks (XSS)
    plugin: dalfox
  - name: Vulnerability Checks (LFI/RFI)
    plugin: crlfi
  - name: Reporting
    plugin: reporting
""",
    "plugins/reporting/reporting_plugin.py": """from core.plugin_manager.interface import ReconXPlugin
from core.schemas import HostProfile
from core.engine.correlation_engine import CorrelationEngine
import json
import os

class ReportingPlugin(ReconXPlugin):
    name = "reporting"
    version = "2.0.0"
    description = "Generate enhanced JSON, HTML, and Markdown reports including vulnerabilities"

    def run(self, target: str, **kwargs):
        context = kwargs.get('context', {})
        results = context.get('all_results', [])
        
        engine = CorrelationEngine()
        engine.ingest(results)
        profiles = engine.get_profiles()
        
        report_data = [p.model_dump() for p in profiles]
        
        os.makedirs("reports", exist_ok=True)
        with open("reports/report.json", "w") as f:
            json.dump(report_data, f, indent=4)
            
        with open("reports/report.md", "w") as f:
            f.write(f"# ReconX WebAssess Report for {target}\\n")
            for p in profiles:
                f.write(f"## {p.domain}\\n")
                f.write(f"### Assets & Infrastructure\\n")
                f.write(f"- IPs: {p.ip}\\n")
                f.write(f"- Ports: {p.ports}\\n")
                f.write(f"- Technologies: {list(set(p.technologies))}\\n\\n")
                
                f.write(f"### Endpoints & Parameters\\n")
                f.write(f"- Endpoints Discovered: {len(p.endpoints)}\\n")
                f.write(f"- Parameters Discovered: {len(p.parameters)}\\n\\n")
                
                f.write(f"### Vulnerabilities\\n")
                if not p.vulnerabilities:
                    f.write("- No vulnerabilities discovered.\\n")
                else:
                    for v in p.vulnerabilities:
                        f.write(f"- **{v.type}** [{v.severity.value}]: {v.url}\\n")
                f.write("\\n")
                
        with open("reports/report.html", "w") as f:
            f.write(f"<html><body><h1>ReconX WebAssess Report for {target}</h1></body></html>")
            
        return {"report_path": "reports/report.json"}
""",
    "tests/web/test_gau.py": """from plugins.web.gau import GauPlugin
from core.schemas import Endpoint, Parameter

def test_gau_plugin():
    plugin = GauPlugin()
    assert plugin.validate() == True
    results = plugin.run("example.com")
    normalized = plugin.normalize(results)
    assert isinstance(normalized, list)
    if normalized:
        has_ep = any(isinstance(i, Endpoint) for i in normalized)
        has_param = any(isinstance(i, Parameter) for i in normalized)
        assert has_ep
""",
    "tests/vulnerabilities/test_dalfox.py": """from plugins.vulnerabilities.dalfox import DalfoxPlugin
from core.schemas import Vulnerability

def test_dalfox_plugin():
    plugin = DalfoxPlugin()
    assert plugin.validate() == True
    results = plugin.run("example.com")
    normalized = plugin.normalize(results)
    assert isinstance(normalized, list)
    if normalized:
        assert isinstance(normalized[0], Vulnerability)
"""
}

def patch_reconx():
    reconx_path = BASE_DIR / "reconx.py"
    if not reconx_path.exists():
        return
    with open(reconx_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    findings_cmd = """
def cmd_findings():
    import os, json
    report_path = "reports/report.json"
    if not os.path.exists(report_path):
        print("No findings report found. Run a webassess workflow first.")
        return
    with open(report_path, "r") as f:
        data = json.load(f)
    print("Vulnerability Findings:")
    for host in data:
        for v in host.get("vulnerabilities", []):
            print(f"[{v.get('severity')}] {v.get('type')} at {v.get('url')}")
"""
    if "def cmd_findings()" not in content:
        content = content.replace("def main():", findings_cmd + "\\ndef main():")
        content = content.replace('"plugins", "run", "workflow"', '"plugins", "run", "workflow", "findings"')
        arg_logic = """
    elif args.command == "findings":
        cmd_findings()
"""
        content = content.replace('    else:\\n        # Full interactive mode', arg_logic + '    else:\\n        # Full interactive mode')
        
    with open(reconx_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    for rel_path, content in FILES.items():
        filepath = BASE_DIR / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        init_file = filepath.parent / "__init__.py"
        if not init_file.exists():
            init_file.touch()

    patch_reconx()
    print("Stage 5 assets (Engine, Workflow, Reporting, Tests, CLI) created successfully.")

if __name__ == "__main__":
    main()
