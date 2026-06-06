import os
from pathlib import Path

BASE_DIR = Path("e:/ReconX/Reconx_V_2.0.0")

FILES = {
    "core/engine/correlation_engine.py": """from core.schemas import OrganizationProfile, Organization, HostProfile, Domain, IPAddress, Port, URL, Technology, DNSRecord, Endpoint, Parameter, Vulnerability, Finding, Employee, Email, Username, PhoneNumber, SocialProfile, Exposure, BreachRecord, ThreatIndicator
from typing import List, Any, Dict

class CorrelationEngine:
    def __init__(self):
        self.organizations: Dict[str, OrganizationProfile] = {}

    def get_or_create_org(self, name: str) -> OrganizationProfile:
        if name not in self.organizations:
            self.organizations[name] = OrganizationProfile(organization=name)
        return self.organizations[name]

    def ingest(self, results: List[Any], org_name: str = "Default Org"):
        org = self.get_or_create_org(org_name)
        # Default host mapping
        default_host = None
        if not org.domains:
            default_host = HostProfile(domain="default")
            org.domains.append(default_host)
        else:
            default_host = org.domains[0]

        for item in results:
            if isinstance(item, Organization):
                # Upgrade name if default
                if org.organization == "Default Org":
                    self.organizations[item.name] = org
                    del self.organizations["Default Org"]
                    org.organization = item.name
            elif isinstance(item, Domain):
                new_host = HostProfile(domain=item.value)
                org.domains.append(new_host)
            elif isinstance(item, Employee):
                org.employees.append(item)
            elif isinstance(item, Email):
                org.emails.append(item)
            elif isinstance(item, Username):
                org.usernames.append(item)
            elif isinstance(item, PhoneNumber):
                org.phone_numbers.append(item)
            elif isinstance(item, SocialProfile):
                org.social_profiles.append(item)
            elif isinstance(item, Exposure):
                org.exposures.append(item)
            elif isinstance(item, BreachRecord):
                org.breach_records.append(item)
            elif isinstance(item, ThreatIndicator):
                org.threat_indicators.append(item)
            # Map technical assets to default host
            elif isinstance(item, Port):
                default_host.ports.append(item.number)
            elif isinstance(item, URL):
                default_host.urls.append(item.value)
            elif isinstance(item, Endpoint):
                default_host.endpoints.append(item)
            elif isinstance(item, Vulnerability):
                default_host.vulnerabilities.append(item)
            elif isinstance(item, Finding):
                default_host.findings.append(item)

    def get_profiles(self) -> List[OrganizationProfile]:
        return list(self.organizations.values())
""",
    "workflows/osint.yaml": """name: OSINT & Intelligence Workflow
description: Organization discovery to threat correlation
steps:
  - name: Organization Discovery
    plugin: acquifinder
  - name: Email Discovery
    plugin: theharvester
  - name: Username Intelligence
    plugin: social_intel
  - name: Breach Intelligence
    plugin: breach-check
  - name: Threat Intelligence
    plugin: threat_intel
  - name: Reporting
    plugin: reporting
""",
    "plugins/reporting/reporting_plugin.py": """from core.plugin_manager.interface import ReconXPlugin
from core.schemas import OrganizationProfile
from core.engine.correlation_engine import CorrelationEngine
import json
import os

class ReportingPlugin(ReconXPlugin):
    name = "reporting"
    version = "3.0.0"
    description = "Generate OSINT enhanced JSON, HTML, and Markdown reports"

    def run(self, target: str, **kwargs):
        context = kwargs.get('context', {})
        results = context.get('all_results', [])
        
        engine = CorrelationEngine()
        engine.ingest(results, org_name=target)
        profiles = engine.get_profiles()
        
        report_data = [p.model_dump() for p in profiles]
        
        os.makedirs("reports", exist_ok=True)
        with open("reports/osint_report.json", "w") as f:
            json.dump(report_data, f, indent=4)
            
        with open("reports/osint_report.md", "w") as f:
            f.write(f"# ReconX Intelligence Report for {target}\\n")
            for p in profiles:
                f.write(f"## Organization: {p.organization}\\n")
                f.write(f"### Emails Discovered: {len(p.emails)}\\n")
                for e in p.emails:
                    f.write(f"- {e.value} (Confidence: {e.confidence.value})\\n")
                f.write(f"\\n### Social Profiles Discovered: {len(p.social_profiles)}\\n")
                for s in p.social_profiles:
                    f.write(f"- {s.platform}: {s.username} ({s.url})\\n")
                f.write(f"\\n### Breach Records: {len(p.breach_records)}\\n")
                for b in p.breach_records:
                    f.write(f"- Source: {b.source} (Type: {b.exposure_type})\\n")
                f.write(f"\\n### Threat Indicators: {len(p.threat_indicators)}\\n")
                for t in p.threat_indicators:
                    f.write(f"- {t.indicator_type.upper()}: {t.value}\\n")
                f.write("\\n---\\n")
                
        with open("reports/osint_report.html", "w") as f:
            f.write(f"<html><body><h1>ReconX Intelligence Report for {target}</h1></body></html>")
            
        return {"report_path": "reports/osint_report.json"}
""",
    "tests/osint/test_theharvester.py": """from plugins.osint.theharvester import TheHarvesterPlugin
from core.schemas import Email, Confidence

def test_theharvester_plugin():
    plugin = TheHarvesterPlugin()
    assert plugin.validate() == True
    results = plugin.run("example.com")
    normalized = plugin.normalize(results)
    assert isinstance(normalized, list)
    if normalized:
        assert isinstance(normalized[0], Email)
        assert normalized[0].confidence == Confidence.HIGH
"""
}

def patch_reconx():
    reconx_path = BASE_DIR / "reconx.py"
    if not reconx_path.exists():
        return
    with open(reconx_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    intelligence_cmd = """
def cmd_intelligence():
    import os, json
    report_path = "reports/osint_report.json"
    if not os.path.exists(report_path):
        print("No OSINT report found. Run an osint workflow first.")
        return
    with open(report_path, "r") as f:
        data = json.load(f)
    print("Intelligence Findings:")
    for org in data:
        print(f"Organization: {org.get('organization')}")
        print(f"  Emails: {len(org.get('emails', []))}")
        print(f"  Breaches: {len(org.get('breach_records', []))}")
        print(f"  Threats: {len(org.get('threat_indicators', []))}")
"""
    if "def cmd_intelligence()" not in content:
        content = content.replace("def main():", intelligence_cmd + "\\ndef main():")
        content = content.replace('"plugins", "run", "workflow", "findings"', '"plugins", "run", "workflow", "findings", "intelligence"')
        arg_logic = """
    elif args.command == "intelligence":
        cmd_intelligence()
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
    print("Stage 6 assets created successfully.")

if __name__ == "__main__":
    main()
