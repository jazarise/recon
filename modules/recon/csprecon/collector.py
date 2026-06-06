import requests
import re
from core.models import Finding

class CspReconCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        self.domain_regex = re.compile(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')

    def collect(self, target: str, **kwargs) -> list:
        findings = []
        if not target.startswith("http"):
            url = f"https://{target}"
        else:
            url = target
            
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            csp = resp.headers.get("Content-Security-Policy", "")
            if csp:
                domains = self.domain_regex.findall(csp)
                for d in set(domains):
                    if d not in ('unsafe-inline', 'unsafe-eval', 'none', 'self'):
                        finding = Finding(
                            category="csp_domain",
                            source="csprecon",
                            value=d,
                            metadata={"target_url": url}
                        )
                        findings.append(finding)
        except Exception:
            pass
        return findings
