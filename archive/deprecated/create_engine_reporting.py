import os
from pathlib import Path

BASE_DIR = Path("e:/ReconX/Reconx_V_2.0.0")

FILES = {
    "core/engine/correlation_engine.py": """from core.schemas import HostProfile, Domain, IPAddress, Port, URL, Technology, DNSRecord
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
                # For simplicity, assuming the value is an IP and mapping it to a global 'target' if we don't have correlation yet
                pass
            elif isinstance(item, Port):
                # Ideally, we map by IP. Mocking correlation by adding to all hosts for now
                for h in self.hosts.values():
                    if item.number not in h.ports:
                        h.ports.append(item.number)
            elif isinstance(item, URL):
                for h in self.hosts.values():
                    h.urls.append(item.value)
                    h.technologies.extend(item.technologies)
            elif isinstance(item, DNSRecord):
                for h in self.hosts.values():
                    h.dns_records.append(item)

    def get_profiles(self) -> List[HostProfile]:
        return list(self.hosts.values())
""",
    "plugins/reporting/reporting_plugin.py": """from core.plugin_manager.interface import ReconXPlugin
from core.schemas import HostProfile
from core.engine.correlation_engine import CorrelationEngine
import json
import os

class ReportingPlugin(ReconXPlugin):
    name = "reporting"
    version = "1.0.0"
    description = "Generate JSON, HTML, and Markdown reports"

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
            f.write(f"# ReconX Report for {target}\\n")
            for p in profiles:
                f.write(f"## {p.domain}\\n")
                f.write(f"- IPs: {p.ip}\\n")
                f.write(f"- Ports: {p.ports}\\n")
                f.write(f"- URLs: {p.urls}\\n")
                f.write(f"- Technologies: {p.technologies}\\n")
                f.write("\\n")
                
        with open("reports/report.html", "w") as f:
            f.write(f"<html><body><h1>ReconX Report for {target}</h1></body></html>")
            
        return {"report_path": "reports/report.json"}
"""
}

def main():
    for rel_path, content in FILES.items():
        filepath = BASE_DIR / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        init_file = filepath.parent / "__init__.py"
        if not init_file.exists():
            init_file.touch()

    print("Engine and reporting created successfully.")

if __name__ == "__main__":
    main()
