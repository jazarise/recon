from core.http.client import HttpClient
import os
import json
import asyncio
import urllib.request
import urllib.error
import ssl
import re
from pathlib import Path


import logging

logger = logging.getLogger("csp_extractor")

DOMAIN_REGEX = re.compile(r"(?i)(?:[_a-z0-9\*](?:[_a-z0-9-\*]{0,61}[a-z0-9])?\.)+(?:[a-z](?:[a-z0-9-]{0,61}[a-z0-9]))+")

CSP_HEADERS = [
    "Content-Security-Policy",
    "Content-Security-Policy-Report-Only",
    "X-Content-Security-Policy",
    "X-WebKit-CSP",
]

class Plugin:
    async def run(target: str, context: dict) -> dict -> dict:
        target = context.get("target")
        if not target:
            raise ValueError("No target provided to csp_extractor")

        project_dir = OUTPUTS_DIR / "projects" / target
        project_dir.mkdir(parents=True, exist_ok=True)
        input_file = project_dir / "alive_urls.txt"
        out_file = project_dir / "csp_domains.txt"

        urls_to_check = set()
        if input_file.exists():
            with open(input_file, "r") as f:
                for line in f:
                    if line.strip(): urls_to_check.add(line.strip())
        else:
            urls_to_check.add(f"https://{target}")

        csp_domains = set()
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Allow parallel requests up to limits using async loops if possible, but for stability we stick to threads or simple loop here with a timeout
        # Extracted improvements from csprecon:
        # 1. Advanced regex for domain matching
        # 2. Support for 4 different CSP headers
        # 3. HTML body meta tag parsing (basic text parsing if BeautifulSoup is missing)
        
        for url in list(urls_to_check)[:100]: # Increased check limit
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
                with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
                    
                    # 1. Header parsing
                    for h in CSP_HEADERS:
                        csp_val = response.headers.get(h)
                        if csp_val:
                            matches = DOMAIN_REGEX.findall(csp_val)
                            csp_domains.update(matches)

                    # 2. Body meta parsing
                    body = response.read(500 * 1024).decode('utf-8', errors='ignore') # limit reading to first 500KB
                    # Looking for <meta http-equiv="Content-Security-Policy" content="...">
                    meta_matches = re.findall(r'<meta[^>]+http-equiv=[\'"]?Content-Security-Policy[\'"]?[^>]+content=[\'"]([^\'"]+)[\'"]', body, re.IGNORECASE)
                    for meta_content in meta_matches:
                        matches = DOMAIN_REGEX.findall(meta_content)
                        csp_domains.update(matches)
                        
            except Exception as e:
                logger.debug(f"Failed to extract CSP from {url}: {e}")

        findings = []
        with open(out_file, "w") as f:
            for dom in sorted(list(csp_domains)):
                # Strip wildcards and basic cleanup
                clean_dom = dom.strip(".*").strip()
                if not clean_dom or " " in clean_dom or len(clean_dom) < 4:
                    continue
                    
                if not any(x in clean_dom for x in ['self', 'none', 'unsafe', 'data:', 'blob:', 'w3.org']):
                    f.write(f"{clean_dom}\n")
                    findings.append({"type": "domain", "name": clean_dom, "source": "csprecon_logic", "host": target})

        return {
            "plugin": "csp_extractor",
            "target": target,
            "domains_found": len(findings),
            "findings": findings
        }
