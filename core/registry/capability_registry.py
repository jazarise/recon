from typing import Dict, List
from .capability_types import Capability, CapabilityCategory, Priority

# Master list of capabilities
CAPABILITIES_LIST = [
    Capability(name="discovery.subdomains", category=CapabilityCategory.DISCOVERY, description="Enumerate subdomains", adapters=["subfinder", "amass", "assetfinder"]),
    Capability(name="discovery.domains", category=CapabilityCategory.DISCOVERY, description="Discover root domains"),
    Capability(name="dns.lookup", category=CapabilityCategory.DNS, description="Resolve DNS records"),
    Capability(name="dns.bruteforce", category=CapabilityCategory.DNS, description="Bruteforce DNS records"),
    Capability(name="dns.zone_transfer", category=CapabilityCategory.DNS, description="Attempt zone transfers"),
    Capability(name="asn.lookup", category=CapabilityCategory.ASN, description="Lookup ASN details"),
    Capability(name="asn.expand", category=CapabilityCategory.ASN, description="Expand IP ranges from ASN"),
    Capability(name="web.probe", category=CapabilityCategory.WEB, description="Probe for live HTTP servers", priority=Priority.HIGH, adapters=["httpx"]),
    Capability(name="web.fingerprint", category=CapabilityCategory.WEB, description="Fingerprint web technologies"),
    Capability(name="web.headers", category=CapabilityCategory.WEB, description="Analyze HTTP headers"),
    Capability(name="content.crawl", category=CapabilityCategory.CONTENT, description="Crawl web content", adapters=["katana", "hakrawler"]),
    Capability(name="content.discovery", category=CapabilityCategory.CONTENT, description="Discover hidden paths"),
    Capability(name="screenshot.capture", category=CapabilityCategory.SCREENSHOT, description="Capture webpage screenshots"),
    Capability(name="osint.organization", category=CapabilityCategory.OSINT, description="Gather organizational intelligence"),
    Capability(name="osint.email", category=CapabilityCategory.OSINT, description="Gather email intelligence"),
    Capability(name="osint.breach", category=CapabilityCategory.OSINT, description="Check for breached credentials"),
    Capability(name="cloud.aws", category=CapabilityCategory.CLOUD, description="Enumerate AWS assets"),
    Capability(name="cloud.azure", category=CapabilityCategory.CLOUD, description="Enumerate Azure assets"),
    Capability(name="cloud.gcp", category=CapabilityCategory.CLOUD, description="Enumerate GCP assets"),
    Capability(name="vuln.xss", category=CapabilityCategory.VULNERABILITY, description="Scan for XSS vulnerabilities", adapters=["dalfox"]),
    Capability(name="vuln.templates", category=CapabilityCategory.VULNERABILITY, description="Run template-based vulnerability scans", adapters=["nuclei"]),
    Capability(name="vuln.csp", category=CapabilityCategory.VULNERABILITY, description="Analyze Content Security Policy"),
    Capability(name="report.html", category=CapabilityCategory.REPORTING, description="Generate HTML reports"),
    Capability(name="report.json", category=CapabilityCategory.REPORTING, description="Generate JSON reports"),
    Capability(name="report.pdf", category=CapabilityCategory.REPORTING, description="Generate PDF reports")
]

class CapabilityRegistry:
    def __init__(self):
        self._capabilities: Dict[str, Capability] = {cap.name: cap for cap in CAPABILITIES_LIST}

    def get_capability(self, name: str) -> Capability:
        return self._capabilities.get(name)

    def list_capabilities(self) -> List[Capability]:
        return list(self._capabilities.values())
    
    def register_adapter(self, capability_name: str, adapter_name: str):
        if capability_name in self._capabilities:
            if adapter_name not in self._capabilities[capability_name].adapters:
                self._capabilities[capability_name].adapters.append(adapter_name)

capability_registry = CapabilityRegistry()
