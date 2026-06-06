import requests
from urllib.parse import urlparse, parse_qs
from core.models import Finding

class S3cXSSerCollector:
    def __init__(self):
        self.headers = {'User-Agent': 'ReconX/2.0'}

    def collect(self, target: str, **kwargs) -> list:
        findings = []
        if not target.startswith("http"):
            target = f"http://{target}"
            
        parsed_url = urlparse(target)
        params = parse_qs(parsed_url.query)
        
        if not params:
            return findings
            
        try:
            resp = requests.get(target, headers=self.headers, timeout=10)
            html = resp.text
            
            for param, values in params.items():
                for val in values:
                    if val and val in html:
                        findings.append(Finding(
                            category="reflected_parameter",
                            source="s3cxsser",
                            value=f"Parameter '{param}' with value '{val}' is reflected in the response",
                            metadata={"target_url": target, "parameter": param, "reflected_value": val}
                        ))
        except Exception:
            pass
            
        return findings
