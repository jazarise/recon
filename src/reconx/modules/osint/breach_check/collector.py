import requests
from reconx.core.models import Finding
from typing import List

class BreachCheckCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def check_leakcheck(self, email: str) -> List[Finding]:
        findings = []
        try:
            resp = requests.get('https://leakcheck.io/api/public', params={'check': email}, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    for source in data.get('sources', []):
                        finding = Finding(
                            category="data_breach",
                            source="leakcheck",
                            value=f"Breach found in {source.get('name', 'Unknown')}",
                            metadata={"email": email, "breach_name": source.get('name')}
                        )
                        findings.append(finding)
        except Exception:
            pass
        return findings

    def check_hudsonrock(self, email: str) -> List[Finding]:
        findings = []
        try:
            resp = requests.get('https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email', params={'email': email}, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                stealers = data.get('stealers', [])
                for stealer in stealers:
                    finding = Finding(
                        category="info_stealer",
                        source="hudsonrock",
                        value=f"Info stealer malware path: {stealer.get('malware_path', 'Unknown')}",
                        metadata={"email": email, "stealer_data": stealer}
                    )
                    findings.append(finding)
        except Exception:
            pass
        return findings

    def collect(self, target: str, **kwargs) -> list:
        # Assuming target is an email
        findings = []
        if "@" in target:
            findings.extend(self.check_leakcheck(target))
            findings.extend(self.check_hudsonrock(target))
        return findings
