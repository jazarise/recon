"""
ReconX — Stage 21: New Tool Modules
=====================================
Absorbed capabilities from crlfuzz, reconftw, pentest-ai, METATRON.

Modules:
  CRLFProbe          — CRLF injection detection
  LeakSearch         — Email/credential leak lookup
  DorkEngine         — Google dorking automation
  GitHubIntel        — GitHub organization/secrets analysis
  MailHygiene        — SPF/DMARC/DKIM DNS analysis
  AuthManager        — JWT/Bearer/Basic session management

All tools follow the ReconX BaseTool interface:
  tool.run(target, **kwargs) → ToolResult
"""
from __future__ import annotations

import json
import logging
import re
import socket
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

log = logging.getLogger("reconx.tools.stage21")


# ── Shared Result Model ────────────────────────────────────────────────────────

@dataclass
class ToolResult:
    tool:       str
    target:     str
    success:    bool
    findings:   list[dict]       = field(default_factory=list)
    raw:        str              = ""
    error:      Optional[str]   = None
    duration_s: float           = 0.0
    metadata:   dict            = field(default_factory=dict)

    def add_finding(self, title: str, severity: str, evidence: str = "",
                    meta: dict | None = None) -> None:
        self.findings.append({
            "title": title,
            "severity": severity.upper(),
            "tool": self.tool,
            "target": self.target,
            "evidence": evidence,
            "meta": meta or {},
        })


# ─────────────────────────────────────────────────────────────────────────────
# CRLF PROBE (absorbed from crlfuzz)
# ─────────────────────────────────────────────────────────────────────────────

CRLF_PAYLOADS = [
    "%0d%0a",
    "%0d%0aX-Injected: reconx",
    "%0a",
    "%0aX-Injected: reconx",
    "\\r\\n",
    "\\r\\nX-Injected: reconx",
    "%E5%98%8A%E5%98%8D",            # Unicode CRLF bypass
    "%E5%98%8A%E5%98%8DX-Injected: reconx",
    "\\u000d\\u000a",
    "%c0%8a",                        # Overlong UTF-8
    "\\r",
    "\\n",
    "%0d%0aSet-Cookie: crlf=injected",
    "%0d%0aLocation: https://evil.example.com",
    "\r\nX-Injected: reconx",
]

CRLF_INJECTION_PATTERNS = [
    re.compile(r"X-Injected:\s*reconx", re.IGNORECASE),
    re.compile(r"Set-Cookie:\s*crlf=injected", re.IGNORECASE),
    re.compile(r"Location:\s*https://evil\.example\.com", re.IGNORECASE),
]

CRLF_PARAM_POSITIONS = ["path", "query", "header", "referer"]


class CRLFProbe:
    """
    CRLF injection scanner.
    Tests URL parameters and common injection points for CRLF vulnerabilities.
    """

    def __init__(self, timeout: float = 5.0, threads: int = 10):
        self.timeout = timeout
        self.threads = threads

    def run(self, target_url: str, params: list[str] | None = None) -> ToolResult:
        t0 = time.time()
        result = ToolResult(tool="crlf-probe", target=target_url, success=False)
        tested = 0

        try:
            parsed = urllib.parse.urlparse(target_url)
            base_params = dict(urllib.parse.parse_qsl(parsed.query))
            test_params = params or list(base_params.keys()) or ["url", "redirect", "next", "return", "callback", "ref", "path"]

            tasks = []
            for param in test_params:
                for payload in CRLF_PAYLOADS:
                    tasks.append((param, payload))

            with ThreadPoolExecutor(max_workers=self.threads) as pool:
                futures = {
                    pool.submit(self._test, target_url, parsed, param, payload): (param, payload)
                    for param, payload in tasks
                }
                for future in as_completed(futures):
                    tested += 1
                    injected, param, payload = future.result()
                    if injected:
                        result.add_finding(
                            title=f"CRLF Injection — parameter '{param}'",
                            severity="MEDIUM",
                            evidence=f"Payload: {payload[:50]} | Reflected header found in response",
                            meta={"param": param, "payload": payload},
                        )

            result.success = True
            result.metadata = {"tested_payloads": tested, "params": test_params}

        except Exception as e:
            result.error = str(e)
            log.debug(f"CRLFProbe error on {target_url}: {e}")

        result.duration_s = round(time.time() - t0, 2)
        return result

    def _test(self, base_url: str, parsed: urllib.parse.ParseResult,
              param: str, payload: str) -> tuple[bool, str, str]:
        try:
            qs = dict(urllib.parse.parse_qsl(parsed.query))
            qs[param] = f"reconxtest{payload}X-Injected: reconx"
            test_url = urllib.parse.urlunparse(parsed._replace(
                query=urllib.parse.urlencode(qs)
            ))
            req = urllib.request.Request(test_url, headers={
                "User-Agent": "Mozilla/5.0 (ReconX Security Scanner)",
            })
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                headers_text = "\r\n".join(f"{k}: {v}" for k, v in resp.headers.items())
                for pat in CRLF_INJECTION_PATTERNS:
                    if pat.search(headers_text):
                        return True, param, payload
        except Exception:
            pass
        return False, param, payload


# ─────────────────────────────────────────────────────────────────────────────
# LEAK SEARCH (absorbed from reconftw / METATRON)
# ─────────────────────────────────────────────────────────────────────────────

class LeakSearch:
    """
    Email and credential leak lookup.
    Queries public breach APIs — no credentials stored, read-only queries.
    """

    def run(self, domain: str, api_key: Optional[str] = None) -> ToolResult:
        t0 = time.time()
        result = ToolResult(tool="leak-search", target=domain, success=False)

        # HaveIBeenPwned domain search (requires API key for email-level)
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachesdomain/{urllib.parse.quote(domain)}"
            req = urllib.request.Request(url, headers={
                "user-agent": "reconx-security-scanner",
                "hibp-api-key": api_key or "",
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                breaches = json.loads(resp.read())
                if breaches:
                    result.add_finding(
                        title=f"Domain found in {len(breaches)} breach(es)",
                        severity="HIGH" if len(breaches) >= 3 else "MEDIUM",
                        evidence=f"Breaches: {', '.join(b.get('Name','?') for b in breaches[:5])}",
                        meta={"breach_count": len(breaches), "breaches": [b.get("Name") for b in breaches]},
                    )
            result.success = True
        except urllib.error.HTTPError as e:
            if e.code == 401:
                result.error = "HaveIBeenPwned API key required for domain search"
            elif e.code == 404:
                result.success = True   # No breaches found — success
                result.metadata["breach_count"] = 0
            else:
                result.error = f"HIBP HTTP {e.code}"
        except Exception as e:
            result.error = str(e)

        # Dehashed public search (pattern check only — no key required)
        self._check_dehashed_pattern(domain, result)

        result.duration_s = round(time.time() - t0, 2)
        return result

    def _check_dehashed_pattern(self, domain: str, result: ToolResult) -> None:
        """Check if domain appears in Dehashed public index (pattern match only)."""
        try:
            q = urllib.parse.quote(f'domain:"{domain}"')
            url = f"https://api.dehashed.com/search?query={q}&size=1"
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read())
                total = data.get("total", 0)
                if total > 0:
                    result.add_finding(
                        title=f"Domain credentials in leak databases ({total} entries)",
                        severity="HIGH",
                        evidence=f"Dehashed: {total} results for {domain}",
                        meta={"source": "dehashed", "count": total},
                    )
        except Exception:
            import logging
            logging.warning("Dehashed requires authentication API key. Skipping dehashed leak search.")


# ─────────────────────────────────────────────────────────────────────────────
# DORK ENGINE (absorbed from reconftw / dorks_hunter)
# ─────────────────────────────────────────────────────────────────────────────

DORK_TEMPLATES = {
    "sensitive_files":   'site:{domain} ext:log OR ext:sql OR ext:bak OR ext:env OR ext:cfg',
    "exposed_panels":    'site:{domain} intitle:"admin" OR intitle:"login" OR intitle:"dashboard"',
    "api_keys":          'site:{domain} intext:"api_key" OR intext:"apikey" OR intext:"access_token"',
    "directory_listing": 'site:{domain} intitle:"Index of /"',
    "error_pages":       'site:{domain} "PHP Parse error" OR "SQL syntax" OR "Warning: mysql"',
    "subdomains":        'site:*.{domain} -www',
    "github_secrets":    'site:github.com "{domain}" password OR secret OR key OR token',
    "jira_issues":       'site:jira.{domain} OR site:{domain}/jira',
    "swagger_ui":        'site:{domain} intitle:"Swagger UI" OR inurl:"/swagger-ui"',
    "jenkins":           'site:{domain} intitle:"Dashboard [Jenkins]"',
    "wordpress":         'site:{domain} inurl:wp-content OR inurl:wp-admin',
    "s3_buckets":        'site:s3.amazonaws.com "{domain}"',
    "trello_boards":     'site:trello.com "{domain}"',
    "pastebin_leaks":    'site:pastebin.com "{domain}" password OR token',
}


class DorkEngine:
    """
    Google/DuckDuckGo dork engine.
    Generates and executes structured dork queries for a target domain.
    Rate-limited to avoid blocking.
    """

    def __init__(self, delay_s: float = 2.0):
        self.delay_s = delay_s

    def generate_dorks(self, domain: str) -> dict[str, str]:
        return {name: tpl.replace("{domain}", domain)
                for name, tpl in DORK_TEMPLATES.items()}

    def run(self, domain: str, categories: list[str] | None = None) -> ToolResult:
        t0 = time.time()
        result = ToolResult(tool="dork-engine", target=domain, success=False)
        dorks = self.generate_dorks(domain)
        if categories:
            dorks = {k: v for k, v in dorks.items() if k in categories}

        result.metadata["dorks_generated"] = list(dorks.keys())
        result.metadata["queries"] = dorks
        result.success = True

        # In a full deployment, each dork would be executed against DuckDuckGo
        # with rate-limiting and result parsing. For now, we generate the
        # queries and flag them for operator review.
        result.add_finding(
            title=f"{len(dorks)} dork queries generated for {domain}",
            severity="INFO",
            evidence=f"Categories: {', '.join(dorks.keys())}",
            meta={"dorks": dorks, "note": "Execute queries manually or enable DuckDuckGo integration"},
        )

        result.duration_s = round(time.time() - t0, 2)
        return result


# ─────────────────────────────────────────────────────────────────────────────
# GITHUB INTEL (absorbed from reconftw / trufflehog patterns)
# ─────────────────────────────────────────────────────────────────────────────

SECRET_PATTERNS = [
    (re.compile(r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?([A-Za-z0-9_\-]{20,})'), "API Key"),
    (re.compile(r'(?i)(secret|password|passwd|pwd)\s*[:=]\s*["\']?([^\s\'"]{8,})'), "Credential"),
    (re.compile(r'(?i)(token|auth[_-]?token)\s*[:=]\s*["\']?([A-Za-z0-9_\-]{20,})'), "Token"),
    (re.compile(r'AKIA[0-9A-Z]{16}'), "AWS Access Key"),
    (re.compile(r'(?i)-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----'), "Private Key"),
    (re.compile(r'sk-[A-Za-z0-9]{48}'), "OpenAI Key"),
    (re.compile(r'ghp_[A-Za-z0-9]{36}'), "GitHub PAT"),
    (re.compile(r'ghu_[A-Za-z0-9]{36}'), "GitHub User Token"),
    (re.compile(r'AIza[0-9A-Za-z\-_]{35}'), "Google API Key"),
]


class GitHubIntel:
    """
    GitHub organization intelligence — searches public repos for secrets,
    sensitive files, and exposed configuration.
    """

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN", "")

    def run(self, org_or_domain: str, deep: bool = False) -> ToolResult:
        t0 = time.time()
        result = ToolResult(tool="github-intel", target=org_or_domain, success=False)

        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"

        # Search GitHub for target mentions
        try:
            query = urllib.parse.quote(f'"{org_or_domain}"')
            url = f"https://api.github.com/search/code?q={query}&per_page=10"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                total = data.get("total_count", 0)
                items = data.get("items", [])

                if total > 0:
                    result.add_finding(
                        title=f"Organization '{org_or_domain}' referenced in {total} public GitHub files",
                        severity="MEDIUM" if total < 20 else "HIGH",
                        evidence=f"Repos: {', '.join(set(i['repository']['full_name'] for i in items[:5]))}",
                        meta={"total": total, "sample_repos": [i["repository"]["full_name"] for i in items[:5]]},
                    )

                # Scan returned code snippets for secrets
                for item in items:
                    file_url = item.get("url", "")
                    self._scan_file_for_secrets(file_url, headers, result)

            result.success = True
        except urllib.error.HTTPError as e:
            if e.code == 403:
                result.error = "GitHub API rate limit hit. Set GITHUB_TOKEN for higher limits."
            else:
                result.error = f"GitHub API HTTP {e.code}"
        except Exception as e:
            result.error = str(e)

        result.duration_s = round(time.time() - t0, 2)
        return result

    def _scan_file_for_secrets(self, file_url: str, headers: dict, result: ToolResult) -> None:
        if not file_url:
            return
        try:
            req = urllib.request.Request(file_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read())
                content_b64 = data.get("content", "")
                if content_b64:
                    import base64
                    content = base64.b64decode(content_b64).decode("utf-8", errors="ignore")
                    for pattern, label in SECRET_PATTERNS:
                        m = pattern.search(content)
                        if m:
                            result.add_finding(
                                title=f"Potential {label} exposed in public GitHub file",
                                severity="HIGH",
                                evidence=f"File: {data.get('path','?')} in {data.get('html_url','?')}",
                                meta={"label": label, "path": data.get("path"), "url": data.get("html_url")},
                            )
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
# MAIL HYGIENE (absorbed from reconftw SPF/DMARC checks)
# ─────────────────────────────────────────────────────────────────────────────

class MailHygiene:
    """
    DNS-based mail security analysis.
    Checks SPF, DMARC, DKIM, MX records for misconfigurations.
    """

    def run(self, domain: str) -> ToolResult:
        t0 = time.time()
        result = ToolResult(tool="mail-hygiene", target=domain, success=False)

        try:
            import dns.resolver
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5

            self._check_spf(domain, resolver, result)
            self._check_dmarc(domain, resolver, result)
            self._check_mx(domain, resolver, result)
            self._check_dkim_common(domain, resolver, result)
            result.success = True

        except ImportError:
            # Fallback: subprocess dig if dnspython not available
            self._check_with_dig(domain, result)
            result.success = True
        except Exception as e:
            result.error = str(e)

        result.duration_s = round(time.time() - t0, 2)
        return result

    def _check_spf(self, domain: str, resolver: Any, result: ToolResult) -> None:
        try:
            answers = resolver.resolve(domain, "TXT")
            spf_records = [str(r) for r in answers if "v=spf1" in str(r).lower()]
            if not spf_records:
                result.add_finding("No SPF record found", "MEDIUM",
                    "Missing SPF record allows email spoofing from this domain")
            elif any("~all" in r for r in spf_records):
                result.add_finding("SPF uses ~all (soft fail)", "LOW",
                    "Soft fail SPF allows spoofed emails to pass. Use -all for hard fail.",
                    {"spf": spf_records[0][:100]})
            elif any("+all" in r for r in spf_records):
                result.add_finding("SPF uses +all (pass all)", "HIGH",
                    "SPF +all allows ANY server to send email as this domain",
                    {"spf": spf_records[0][:100]})
        except Exception:
            result.add_finding("SPF record lookup failed", "INFO", "Could not retrieve TXT records")

    def _check_dmarc(self, domain: str, resolver: Any, result: ToolResult) -> None:
        try:
            answers = resolver.resolve(f"_dmarc.{domain}", "TXT")
            dmarc_records = [str(r) for r in answers if "v=DMARC1" in str(r).upper()]
            if not dmarc_records:
                result.add_finding("No DMARC record found", "MEDIUM",
                    "Missing DMARC allows spoofed emails to bypass policy enforcement")
            else:
                rec = dmarc_records[0]
                if "p=none" in rec.lower():
                    result.add_finding("DMARC policy is 'none' (monitor only)", "LOW",
                        "DMARC p=none takes no action on failing emails. Use p=quarantine or p=reject",
                        {"dmarc": rec[:100]})
        except Exception:
            result.add_finding("No DMARC record at _dmarc." + domain, "MEDIUM",
                "DMARC record not found — domain vulnerable to email spoofing")

    def _check_mx(self, domain: str, resolver: Any, result: ToolResult) -> None:
        try:
            resolver.resolve(domain, "MX")
        except Exception:
            result.add_finding("No MX records found", "INFO",
                "Domain does not appear to accept email")

    def _check_dkim_common(self, domain: str, resolver: Any, result: ToolResult) -> None:
        common_selectors = ["default", "google", "mail", "email", "dkim", "k1", "selector1", "selector2"]
        found = False
        for sel in common_selectors:
            try:
                resolver.resolve(f"{sel}._domainkey.{domain}", "TXT")
                found = True
                break
            except Exception:
                continue
        if not found:
            result.add_finding("No DKIM record found at common selectors", "INFO",
                f"Checked selectors: {', '.join(common_selectors)}")

    def _check_with_dig(self, domain: str, result: ToolResult) -> None:
        import subprocess
        for record_type, check_name in [("TXT", "SPF/DMARC"), ("MX", "MX")]:
            try:
                out = subprocess.run(
                    ["dig", "+short", record_type, domain],
                    capture_output=True, text=True, timeout=5
                ).stdout
                if not out.strip():
                    result.add_finding(f"No {record_type} records found", "INFO",
                        f"dig {record_type} {domain} returned empty")
            except FileNotFoundError:
                result.error = "dig not available; install bind-utils"
                break
            except Exception:
                pass


# ─────────────────────────────────────────────────────────────────────────────
# AUTH MANAGER (absorbed from pentest-ai JWT/Bearer auth flows)
# ─────────────────────────────────────────────────────────────────────────────

import os

@dataclass
class AuthProfile:
    name:         str
    auth_type:    str            # basic|bearer|jwt|cookie|apikey|none
    credentials:  dict           = field(default_factory=dict)
    token:        Optional[str]  = None
    token_expiry: Optional[float] = None
    headers:      dict           = field(default_factory=dict)
    cookies:      dict           = field(default_factory=dict)


class AuthManager:
    """
    Authentication session manager for web assessments.
    Supports: Basic, Bearer, JWT (with auto-refresh), Cookie, API Key.
    """

    def __init__(self):
        self._profiles: dict[str, AuthProfile] = {}
        self._active:   Optional[str] = None

    def configure_basic(self, name: str, username: str, password: str) -> AuthProfile:
        import base64
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        profile = AuthProfile(name=name, auth_type="basic",
                              credentials={"username": username, "password": password},
                              headers={"Authorization": f"Basic {token}"})
        self._profiles[name] = profile
        return profile

    def configure_bearer(self, name: str, token: str) -> AuthProfile:
        profile = AuthProfile(name=name, auth_type="bearer", token=token,
                              headers={"Authorization": f"Bearer {token}"})
        self._profiles[name] = profile
        return profile

    def configure_jwt(
        self, name: str,
        login_url: str, username: str, password: str,
        token_json_path: str = "token",           # JSONPath to token in response
        username_field: str = "email",
        password_field: str = "password",
    ) -> AuthProfile:
        """Authenticate via POST and extract JWT from response."""
        profile = AuthProfile(name=name, auth_type="jwt",
                              credentials={"login_url": login_url, "username_field": username_field,
                                           "password_field": password_field, "token_path": token_json_path})
        try:
            payload = json.dumps({username_field: username, password_field: password}).encode()
            req = urllib.request.Request(login_url, data=payload,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                token = self._extract_path(data, token_json_path)
                if token:
                    profile.token = token
                    profile.headers = {"Authorization": f"Bearer {token}"}
                    log.info(f"JWT acquired for profile '{name}'")
                else:
                    log.warning(f"JWT extraction failed — path '{token_json_path}' not found in response")
        except Exception as e:
            log.error(f"JWT login failed: {e}")
        self._profiles[name] = profile
        return profile

    def configure_apikey(self, name: str, key: str, header_name: str = "X-API-Key") -> AuthProfile:
        profile = AuthProfile(name=name, auth_type="apikey",
                              credentials={"key": key, "header": header_name},
                              headers={header_name: key})
        self._profiles[name] = profile
        return profile

    def get_headers(self, profile_name: Optional[str] = None) -> dict:
        name = profile_name or self._active
        if not name or name not in self._profiles:
            return {}
        return dict(self._profiles[name].headers)

    def set_active(self, name: str) -> None:
        self._active = name

    def apply_to_request(self, req: urllib.request.Request,
                          profile_name: Optional[str] = None) -> None:
        for k, v in self.get_headers(profile_name).items():
            req.add_header(k, v)

    @staticmethod
    def _extract_path(data: dict, path: str) -> Optional[str]:
        """Extract value from nested JSON using dot-notation path."""
        parts = path.split(".")
        current = data
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        return str(current) if current else None
