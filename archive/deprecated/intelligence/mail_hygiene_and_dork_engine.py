"""
ReconX — Mail Hygiene + Dork Engine
======================================
Two modules absorbed from reconftw:
  MailHygiene   — SPF, DMARC, DKIM, MX, BIMI analysis
  DorkEngine    — Google/DuckDuckGo dork query generation and dispatch

Both produce structured findings in ReconX finding schema.
"""
from __future__ import annotations

import logging
import re
import socket
import subprocess
import time
from dataclasses import dataclass, field
from typing import Optional

log = logging.getLogger("reconx.tools.dns.mail_hygiene")

# ═════════════════════════════════════════════════════════════════════════════
# MAIL HYGIENE
# Absorbed from reconftw: check_spf(), check_dmarc(), check_dkim()
# ═════════════════════════════════════════════════════════════════════════════

@dataclass
class MailFinding:
    check:       str
    severity:    str    # CRITICAL | HIGH | MEDIUM | LOW | INFO
    title:       str
    evidence:    str
    remediation: str


@dataclass
class MailHygieneResult:
    domain:   str
    success:  bool
    findings: list[MailFinding] = field(default_factory=list)
    raw:      dict              = field(default_factory=dict)
    error:    str               = ""

    def to_reconx_findings(self) -> list[dict]:
        return [
            {
                "title":       f.title,
                "severity":    f.severity,
                "target":      self.domain,
                "service":     "DNS/Mail",
                "description": f.evidence,
                "remediation": f.remediation,
                "meta":        {"check": f.check},
            }
            for f in self.findings
        ]


# ── DNS TXT lookup helper ─────────────────────────────────────────────────────

def _dig_txt(name: str, timeout: int = 5) -> list[str]:
    """Query TXT records for a DNS name. Returns list of record strings."""
    try:
        import dns.resolver
        resolver = dns.resolver.Resolver()
        resolver.lifetime = timeout
        answers = resolver.resolve(name, "TXT")
        return [str(r).strip('"') for r in answers]
    except ImportError:
        import logging
        logging.info("Falling back to subprocess dig for DNS zone transfer...")

    try:
        r = subprocess.run(
            ["dig", "+short", "TXT", name],
            capture_output=True, text=True, timeout=timeout,
        )
        return [l.strip().strip('"') for l in r.stdout.splitlines() if l.strip()]
    except FileNotFoundError:
        log.debug("Neither dnspython nor dig available")
        return []
    except Exception:
        return []


def _dig_mx(domain: str, timeout: int = 5) -> list[str]:
    try:
        import dns.resolver
        resolver = dns.resolver.Resolver()
        resolver.lifetime = timeout
        answers = resolver.resolve(domain, "MX")
        return [str(r.exchange).rstrip(".") for r in answers]
    except ImportError:
        pass

    try:
        r = subprocess.run(
            ["dig", "+short", "MX", domain],
            capture_output=True, text=True, timeout=timeout,
        )
        return [l.strip() for l in r.stdout.splitlines() if l.strip()]
    except Exception:
        return []


class MailHygiene:
    """
    Full mail security analysis: SPF, DMARC, DKIM, MX, BIMI.
    Absorbed from reconftw check_spf/check_dmarc functions.

    Works with dnspython if installed; falls back to dig subprocess.
    """

    _DKIM_COMMON_SELECTORS = [
        "default", "google", "mail", "email", "dkim", "k1",
        "selector1", "selector2", "s1", "s2", "smtp",
        "key1", "key2", "protonmail", "zoho", "sendgrid",
        "amazonses", "mandrill", "mailchimp", "postfix",
    ]

    def run(self, domain: str) -> MailHygieneResult:
        result = MailHygieneResult(domain=domain, success=False)

        try:
            self._check_mx(domain, result)
            self._check_spf(domain, result)
            self._check_dmarc(domain, result)
            self._check_dkim(domain, result)
            self._check_bimi(domain, result)
            result.success = True
        except Exception as e:
            result.error = str(e)
            log.debug("MailHygiene error on %s: %s", domain, e)

        return result

    def _check_mx(self, domain: str, result: MailHygieneResult) -> None:
        mx_records = _dig_mx(domain)
        result.raw["mx"] = mx_records
        if not mx_records:
            result.findings.append(MailFinding(
                check="mx",
                severity="INFO",
                title="No MX records found",
                evidence=f"Domain {domain} has no MX records — does not receive email",
                remediation="If email is expected, configure MX records.",
            ))
        else:
            result.findings.append(MailFinding(
                check="mx",
                severity="INFO",
                title=f"MX records found ({len(mx_records)})",
                evidence=f"MX servers: {', '.join(mx_records[:5])}",
                remediation="Verify all MX servers are expected and current.",
            ))

    def _check_spf(self, domain: str, result: MailHygieneResult) -> None:
        txts = _dig_txt(domain)
        spf_records = [t for t in txts if t.lower().startswith("v=spf1")]
        result.raw["spf"] = spf_records

        if not spf_records:
            result.findings.append(MailFinding(
                check="spf",
                severity="MEDIUM",
                title="No SPF record found",
                evidence=f"No SPF TXT record at {domain}. Any server can send email as this domain.",
                remediation=(
                    "Add SPF record: v=spf1 include:_spf.google.com ~all\n"
                    "Use -all (hard fail) for strictest enforcement."
                ),
            ))
            return

        if len(spf_records) > 1:
            result.findings.append(MailFinding(
                check="spf",
                severity="MEDIUM",
                title="Multiple SPF records found",
                evidence=f"Multiple SPF records cause undefined behavior: {spf_records}",
                remediation="Merge all SPF records into a single TXT record.",
            ))

        spf = spf_records[0]

        if "+all" in spf:
            result.findings.append(MailFinding(
                check="spf",
                severity="HIGH",
                title="SPF uses +all (pass all senders)",
                evidence=f"SPF record ends with +all — allows ANY server to send email as {domain}",
                remediation="Change +all to -all (hard fail) or ~all (soft fail).",
            ))
        elif "~all" in spf:
            result.findings.append(MailFinding(
                check="spf",
                severity="LOW",
                title="SPF uses ~all (soft fail only)",
                evidence=f"Soft fail allows spoofed emails to be delivered (marked, not rejected): {spf}",
                remediation="Consider changing ~all to -all for stricter enforcement.",
            ))
        elif "-all" in spf:
            result.findings.append(MailFinding(
                check="spf",
                severity="INFO",
                title="SPF configured correctly (-all)",
                evidence=f"Hard fail configured: {spf}",
                remediation="No action required. Monitor for legitimate senders not in SPF.",
            ))
        elif "?all" in spf:
            result.findings.append(MailFinding(
                check="spf",
                severity="MEDIUM",
                title="SPF uses ?all (neutral — no enforcement)",
                evidence=f"?all provides no protection against email spoofing: {spf}",
                remediation="Change ?all to -all or ~all.",
            ))

        # Check for too many DNS lookups (SPF limit is 10)
        lookup_mechanisms = re.findall(r"\b(include|a|mx|exists|redirect):", spf, re.IGNORECASE)
        if len(lookup_mechanisms) > 8:
            result.findings.append(MailFinding(
                check="spf",
                severity="LOW",
                title="SPF record approaching DNS lookup limit",
                evidence=f"{len(lookup_mechanisms)} DNS-lookup mechanisms found (limit is 10)",
                remediation="Flatten SPF record using a tool like dmarcian SPF Surveyor.",
            ))

    def _check_dmarc(self, domain: str, result: MailHygieneResult) -> None:
        dmarc_name = f"_dmarc.{domain}"
        txts = _dig_txt(dmarc_name)
        dmarc_records = [t for t in txts if t.upper().startswith("V=DMARC1")]
        result.raw["dmarc"] = dmarc_records

        if not dmarc_records:
            result.findings.append(MailFinding(
                check="dmarc",
                severity="MEDIUM",
                title="No DMARC record found",
                evidence=f"No DMARC record at {dmarc_name}. SPF/DKIM failures not enforced.",
                remediation=(
                    "Add DMARC TXT record at _dmarc.<domain>:\n"
                    "v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com; pct=100"
                ),
            ))
            return

        dmarc = dmarc_records[0]
        result.raw["dmarc_parsed"] = dmarc

        # Parse policy
        p_match = re.search(r"\bp=(\w+)", dmarc, re.IGNORECASE)
        policy  = p_match.group(1).lower() if p_match else "none"

        if policy == "none":
            result.findings.append(MailFinding(
                check="dmarc",
                severity="LOW",
                title="DMARC policy is p=none (monitor only)",
                evidence=f"DMARC p=none takes NO enforcement action on failing emails: {dmarc}",
                remediation="Change p=none to p=quarantine then p=reject after monitoring period.",
            ))
        elif policy == "quarantine":
            result.findings.append(MailFinding(
                check="dmarc",
                severity="INFO",
                title="DMARC policy is p=quarantine",
                evidence=f"Spoofed emails are sent to spam (not rejected): {dmarc}",
                remediation="Consider upgrading to p=reject for maximum protection.",
            ))
        elif policy == "reject":
            result.findings.append(MailFinding(
                check="dmarc",
                severity="INFO",
                title="DMARC policy is p=reject (best practice)",
                evidence=f"Spoofed emails are rejected at gateway: {dmarc}",
                remediation="No action required. Ensure rua/ruf reporting is configured.",
            ))

        # Check percentage
        pct_match = re.search(r"\bpct=(\d+)", dmarc, re.IGNORECASE)
        pct = int(pct_match.group(1)) if pct_match else 100
        if pct < 100 and policy in ("quarantine", "reject"):
            result.findings.append(MailFinding(
                check="dmarc",
                severity="LOW",
                title=f"DMARC only applied to {pct}% of emails",
                evidence=f"pct={pct} means {100-pct}% of spoofed emails bypass DMARC policy",
                remediation="Increase pct=100 when confident all legitimate mail is DMARC-compliant.",
            ))

        # Check reporting
        if "rua=" not in dmarc.lower():
            result.findings.append(MailFinding(
                check="dmarc",
                severity="INFO",
                title="DMARC aggregate reporting not configured",
                evidence="No rua= tag — no email reports on DMARC failures",
                remediation="Add rua=mailto:dmarc@yourdomain.com for aggregate reports.",
            ))

    def _check_dkim(self, domain: str, result: MailHygieneResult) -> None:
        found_selectors: list[str] = []

        for selector in self._DKIM_COMMON_SELECTORS:
            dkim_name = f"{selector}._domainkey.{domain}"
            txts = _dig_txt(dkim_name)
            if any("v=DKIM1" in t.upper() or "k=rsa" in t.lower() for t in txts):
                found_selectors.append(selector)

        result.raw["dkim_selectors"] = found_selectors

        if not found_selectors:
            result.findings.append(MailFinding(
                check="dkim",
                severity="LOW",
                title="No DKIM selectors found at common names",
                evidence=f"Checked {len(self._DKIM_COMMON_SELECTORS)} common selectors — none responded",
                remediation=(
                    "Configure DKIM signing for your mail server.\n"
                    "Generate key: opendkim-genkey -t -s mail -d " + domain
                ),
            ))
        else:
            result.findings.append(MailFinding(
                check="dkim",
                severity="INFO",
                title=f"DKIM configured — {len(found_selectors)} selector(s) found",
                evidence=f"Active selectors: {', '.join(found_selectors)}",
                remediation="Rotate DKIM keys periodically (recommended: every 6-12 months).",
            ))

    def _check_bimi(self, domain: str, result: MailHygieneResult) -> None:
        bimi_name = f"default._bimi.{domain}"
        txts = _dig_txt(bimi_name)
        bimi_records = [t for t in txts if t.upper().startswith("V=BIMI1")]

        result.raw["bimi"] = bimi_records
        if bimi_records:
            result.findings.append(MailFinding(
                check="bimi",
                severity="INFO",
                title="BIMI record configured",
                evidence=f"Brand Indicators for Message Identification found: {bimi_records[0][:80]}",
                remediation="Verify VMC certificate is valid and SVG logo meets BIMI requirements.",
            ))


# ═════════════════════════════════════════════════════════════════════════════
# DORK ENGINE
# Absorbed from reconftw: dork queries, category templates, rate-limited dispatch
# ═════════════════════════════════════════════════════════════════════════════

log2 = logging.getLogger("reconx.tools.osint.dork_engine")

_DORK_TEMPLATES: dict[str, str] = {
    "sensitive_files":       'site:{domain} ext:log OR ext:sql OR ext:bak OR ext:env OR ext:cfg OR ext:conf OR ext:ini OR ext:yaml',
    "admin_panels":          'site:{domain} intitle:"admin" OR intitle:"login" OR intitle:"dashboard" OR intitle:"control panel"',
    "api_keys_exposed":      'site:{domain} intext:"api_key" OR intext:"apikey" OR intext:"access_token" OR intext:"client_secret"',
    "directory_listing":     'site:{domain} intitle:"Index of /" OR intitle:"Directory listing"',
    "error_messages":        'site:{domain} "PHP Parse error" OR "SQL syntax" OR "Warning: mysql_" OR "ORA-" OR "Traceback"',
    "subdomains":            'site:*.{domain} -www -mail',
    "github_exposure":       'site:github.com "{domain}" password OR secret OR key OR token OR credential',
    "jira_confluence":       'site:{domain}/jira OR site:{domain}/confluence OR site:jira.{domain}',
    "swagger_openapi":       'site:{domain} intitle:"Swagger UI" OR inurl:"/swagger-ui" OR inurl:"/api-docs"',
    "jenkins":               'site:{domain} intitle:"Dashboard [Jenkins]" OR inurl:"/jenkins"',
    "wordpress_exposure":    'site:{domain} inurl:wp-content OR inurl:wp-admin OR inurl:xmlrpc.php',
    "s3_buckets":            'site:s3.amazonaws.com "{domain}" OR site:{domain}.s3.amazonaws.com',
    "trello_boards":         'site:trello.com "{domain}"',
    "pastebin_leaks":        'site:pastebin.com "{domain}" password OR token OR secret',
    "gitlab_exposure":       'site:gitlab.com "{domain}" password OR secret OR config',
    "bitbucket_exposure":    'site:bitbucket.org "{domain}" password OR secret OR key',
    "shodan_exposure":       'site:shodan.io "hostname:{domain}"',
    "certificates":          'site:crt.sh "{domain}"',
    "wayback_urls":          'site:web.archive.org "{domain}"',
    "exposed_phpinfo":       'site:{domain} intitle:"phpinfo()" OR inurl:phpinfo.php',
    "spring_actuator":       'site:{domain} inurl:/actuator OR inurl:/actuator/env OR inurl:/actuator/beans',
    "git_exposed":           'site:{domain} inurl:/.git/HEAD OR inurl:/.git/config',
    "docker_registry":       'site:{domain} inurl:v2 intitle:"Docker Registry" OR inurl:/v2/catalog',
    "kubernetes":            'site:{domain} inurl:dashboard intitle:"Kubernetes" OR inurl:/api/v1/namespaces',
}


@dataclass
class DorkResult:
    domain:      str
    category:    str
    query:       str
    results:     list[dict]     = field(default_factory=list)
    executed:    bool           = False
    error:       str            = ""


class DorkEngine:
    """
    Google/DuckDuckGo dork engine.
    Generates structured dork queries and optionally dispatches them via DDG.

    Absorbed from reconftw dork functions and google-hacking-database patterns.

    Usage:
        engine = DorkEngine()
        queries = engine.generate("example.com")          # generate only
        results = engine.run("example.com", execute=True) # generate + search DDG
    """

    def __init__(self, delay_between_queries: float = 3.0):
        self._delay = delay_between_queries

    def generate(
        self, domain: str,
        categories: Optional[list[str]] = None,
    ) -> dict[str, str]:
        """
        Generate dork queries for a domain.

        Args:
            domain:     Target domain (e.g. example.com)
            categories: Subset of categories (default: all)

        Returns:
            dict mapping category → dork query string
        """
        selected = _DORK_TEMPLATES
        if categories:
            selected = {k: v for k, v in _DORK_TEMPLATES.items()
                        if k in categories}

        return {cat: tpl.replace("{domain}", domain)
                for cat, tpl in selected.items()}

    def run(
        self, domain: str,
        categories: Optional[list[str]] = None,
        execute: bool = False,
        max_results_per_query: int = 5,
    ) -> list[DorkResult]:
        """
        Generate dork queries and optionally execute them via DuckDuckGo.

        Args:
            domain:               Target domain
            categories:           Categories to run (default: all)
            execute:              If True, search DDG for each query
            max_results_per_query: DDG results per dork

        Returns:
            List of DorkResult objects
        """
        queries  = self.generate(domain, categories)
        results  = []

        for cat, query in queries.items():
            dr = DorkResult(domain=domain, category=cat, query=query)

            if execute:
                log2.info("Dork [%s]: %s", cat, query[:60])
                try:
                    from .intelligence_search import web_search
                    raw = web_search(query, max_results=max_results_per_query)
                    dr.results = self._parse_ddg_response(raw)
                    dr.executed = True
                except ImportError:
                    # intelligence_search not available — mark as not executed
                    dr.error = "intelligence_search module not available"
                    dr.executed = False
                except Exception as e:
                    dr.error = str(e)

                time.sleep(self._delay)

            results.append(dr)

        return results

    def to_reconx_findings(self, results: list[DorkResult]) -> list[dict]:
        """Convert dork results into ReconX finding schema."""
        findings = []
        for dr in results:
            if dr.results:
                findings.append({
                    "title":       f"Dork results found — {dr.category.replace('_', ' ').title()}",
                    "severity":    self._category_severity(dr.category),
                    "target":      dr.domain,
                    "service":     "OSINT/Dork",
                    "description": f"Query: {dr.query}\nFound {len(dr.results)} results",
                    "evidence":    "\n".join(f"- {r.get('url','?')}: {r.get('snippet','')[:80]}"
                                            for r in dr.results[:3]),
                    "remediation": self._category_remediation(dr.category),
                    "meta":        {"category": dr.category, "query": dr.query,
                                   "result_count": len(dr.results)},
                })
            elif not dr.executed:
                # Query not executed — include as reference for manual use
                findings.append({
                    "title":       f"Dork query generated — {dr.category.replace('_', ' ').title()}",
                    "severity":    "INFO",
                    "target":      dr.domain,
                    "service":     "OSINT/Dork",
                    "description": f"Manual search recommended:\n{dr.query}",
                    "evidence":    f"Run this query in Google: {dr.query}",
                    "remediation": self._category_remediation(dr.category),
                    "meta":        {"category": dr.category, "query": dr.query},
                })
        return findings

    @staticmethod
    def _parse_ddg_response(raw: str) -> list[dict]:
        """Parse web_search() string output into list of {url, title, snippet}."""
        results = []
        current: dict = {}
        for line in raw.splitlines():
            if re.match(r"\[\d+\]", line.strip()):
                if current:
                    results.append(current)
                current = {"title": line.strip()}
            elif line.strip().startswith("URL"):
                current["url"] = line.split(":", 1)[-1].strip()
            elif line.strip().startswith("Snippet"):
                current["snippet"] = line.split(":", 1)[-1].strip()
        if current:
            results.append(current)
        return results

    @staticmethod
    def _category_severity(category: str) -> str:
        high_risk = {
            "sensitive_files", "api_keys_exposed", "git_exposed",
            "docker_registry", "spring_actuator", "github_exposure",
            "pastebin_leaks", "gitlab_exposure", "bitbucket_exposure",
        }
        medium_risk = {
            "admin_panels", "directory_listing", "error_messages",
            "exposed_phpinfo", "jenkins", "kubernetes", "s3_buckets",
        }
        if category in high_risk:
            return "HIGH"
        if category in medium_risk:
            return "MEDIUM"
        return "LOW"

    @staticmethod
    def _category_remediation(category: str) -> str:
        remediations = {
            "sensitive_files":   "Remove sensitive files from web root. Use .htaccess or nginx deny rules.",
            "admin_panels":      "Restrict admin panel access by IP. Enable MFA. Change default URLs.",
            "api_keys_exposed":  "Rotate exposed credentials immediately. Use environment variables.",
            "directory_listing": "Disable directory listing in web server config (Options -Indexes).",
            "error_messages":    "Suppress detailed error messages in production. Use generic error pages.",
            "git_exposed":       "Deny access to /.git/ in web server config. Use .htaccess: Deny from all.",
            "github_exposure":   "Rotate any exposed credentials. Make repositories private if needed.",
            "spring_actuator":   "Restrict /actuator endpoints. Disable sensitive endpoints in production.",
            "s3_buckets":        "Set S3 bucket ACL to private. Enable Block Public Access settings.",
            "jenkins":           "Restrict Jenkins to internal network. Enable authentication.",
            "wordpress_exposure":"Update WordPress/plugins. Restrict wp-admin by IP.",
            "exposed_phpinfo":   "Remove phpinfo() files from production. Never expose PHP configuration.",
            "docker_registry":   "Require authentication for Docker registry. Restrict network access.",
        }
        return remediations.get(
            category,
            "Review findings and restrict access to sensitive resources."
        )
