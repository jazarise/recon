"""
ReconX — Intelligence Search Engine
=====================================
Absorbed from METATRON/search.py — full working implementation.

Provides:
  web_search()            — DuckDuckGo search, no API key needed
  search_cve()            — CVE lookup via DDG + MITRE direct fetch
  search_exploit()        — Exploit search for service+version
  search_fix()            — Mitigation/patch search
  fetch_page()            — URL fetch + HTML text extraction
  handle_search_dispatch()— Smart router (CVE / exploit / fix / general)

Used by the agentic loop when the LLM writes [SEARCH: query].
No external API keys required for basic operation.
"""
from __future__ import annotations

import logging
import re
import time
import urllib.parse
import urllib.request
from typing import Optional

log = logging.getLogger("reconx.ai.intelligence_search")

_DDG_URL   = "https://html.duckduckgo.com/html/"
_UA        = "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
_TIMEOUT   = 15

# ── DuckDuckGo HTML scraper (no API key) ─────────────────────────────────────

def web_search(query: str, max_results: int = 5) -> str:
    """
    Search DuckDuckGo via HTML scraping and return formatted results.
    No API key. No JS required. Falls back gracefully.
    """
    log.info("DDG search: %s", query)
    try:
        data = urllib.parse.urlencode({"q": query, "b": "", "kl": "us-en"}).encode()
        req  = urllib.request.Request(
            _DDG_URL,
            data=data,
            headers={"User-Agent": _UA, "Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        log.debug("DDG fetch error: %s", e)
        return f"[!] Search failed: {e}"

    results = _parse_ddg_html(html, max_results)
    if not results:
        return f"[!] No results for: {query}"

    out = f"[WEB SEARCH: {query}]\n" + "─" * 50 + "\n"
    for i, r in enumerate(results, 1):
        out += f"\n[{i}] {r['title']}\n"
        out += f"    URL     : {r['url']}\n"
        out += f"    Snippet : {r['snippet']}\n"
    return out


def _parse_ddg_html(html: str, limit: int) -> list[dict]:
    """Parse DuckDuckGo HTML result page into structured list."""
    results = []
    # Match result blocks
    blocks = re.findall(
        r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.+?)</a>.*?'
        r'<a[^>]+class="result__snippet"[^>]*>(.+?)</a>',
        html, re.DOTALL
    )
    for url, title, snippet in blocks[:limit]:
        clean_title   = re.sub(r"<[^>]+>", "", title).strip()
        clean_snippet = re.sub(r"<[^>]+>", "", snippet).strip()
        # DDG wraps URLs in redirect — extract real URL
        real_url = _unwrap_ddg_url(url)
        results.append({"url": real_url, "title": clean_title, "snippet": clean_snippet})

    # Fallback: try simpler pattern if the above yields nothing
    if not results:
        titles   = re.findall(r'class="result__a"[^>]*>([^<]+)<', html)
        urls     = re.findall(r'class="result__url"[^>]*>([^<]+)<', html)
        snippets = re.findall(r'class="result__snippet"[^>]*>([^<]+)<', html)
        for i in range(min(limit, len(titles))):
            results.append({
                "url":     urls[i].strip() if i < len(urls) else "",
                "title":   titles[i].strip(),
                "snippet": snippets[i].strip() if i < len(snippets) else "",
            })
    return results


def _unwrap_ddg_url(raw: str) -> str:
    """DDG wraps links in /l/?uddg= redirect — extract original URL."""
    if "uddg=" in raw:
        try:
            qs  = urllib.parse.parse_qs(urllib.parse.urlparse(raw).query)
            url = qs.get("uddg", [raw])[0]
            return urllib.parse.unquote(url)
        except Exception:
            pass
    return raw


# ── CVE Lookup ────────────────────────────────────────────────────────────────

def search_cve(cve_id: str) -> str:
    """
    Look up a specific CVE:
      1. DuckDuckGo search for exploit/details
      2. Direct MITRE CVE fetch
      3. NVD API (optional, no key needed for basic)
    """
    cve_id = cve_id.strip().upper()
    log.info("CVE lookup: %s", cve_id)

    ddg = web_search(f"{cve_id} vulnerability exploit details CVSS", max_results=4)
    mitre = _fetch_mitre(cve_id)
    nvd   = _fetch_nvd(cve_id)

    out  = ddg
    out += f"\n[MITRE: {cve_id}]\n{'─'*40}\n{mitre}\n"
    if nvd:
        out += f"\n[NVD: {cve_id}]\n{'─'*40}\n{nvd}\n"
    return out


def _fetch_mitre(cve_id: str) -> str:
    url = f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}"
    return fetch_page(url, max_chars=1500)


def _fetch_nvd(cve_id: str) -> str:
    """NVD API v2 — no key needed for basic queries."""
    try:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=10) as resp:
            import json
            data = json.loads(resp.read())
        vulns = data.get("vulnerabilities", [])
        if not vulns:
            return ""
        cve_data = vulns[0].get("cve", {})
        desc = next(
            (d["value"] for d in cve_data.get("descriptions", []) if d["lang"] == "en"),
            ""
        )
        metrics = cve_data.get("metrics", {})
        cvss_v3 = metrics.get("cvssMetricV31", metrics.get("cvssMetricV30", []))
        score = ""
        if cvss_v3:
            score = f"CVSS: {cvss_v3[0].get('cvssData', {}).get('baseScore', '?')} " \
                    f"({cvss_v3[0].get('cvssData', {}).get('baseSeverity', '?')})"
        return f"{score}\n{desc[:600]}" if desc else ""
    except Exception as e:
        log.debug("NVD fetch error: %s", e)
        return ""


# ── Exploit Search ────────────────────────────────────────────────────────────

def search_exploit(service: str, version: str) -> str:
    """Search for known exploits for a service + version combination."""
    query = f"{service} {version} exploit CVE vulnerability 2023 2024 2025"
    return web_search(query, max_results=5)


# ── Fix / Mitigation Search ───────────────────────────────────────────────────

def search_fix(vuln_name: str) -> str:
    """Search for mitigation / patch guidance for a vulnerability."""
    query = f"how to fix {vuln_name} security mitigation patch hardening"
    return web_search(query, max_results=3)


# ── Page Fetcher ──────────────────────────────────────────────────────────────

def fetch_page(url: str, max_chars: int = 3000) -> str:
    """
    Fetch a URL and return extracted plain text, stripped of HTML.
    Safe — strips scripts, nav, footer. Truncated to max_chars.
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            raw_html = resp.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return f"[!] HTTP {e.code}: {url}"
    except urllib.error.URLError as e:
        return f"[!] URL error: {e.reason}"
    except Exception as e:
        return f"[!] Fetch error: {e}"

    text = _extract_text(raw_html)
    if len(text) > max_chars:
        text = text[:max_chars] + f"\n... [truncated at {max_chars} chars]"
    return text


def _extract_text(html: str) -> str:
    """Extract readable text from HTML without BeautifulSoup dependency."""
    # Remove script / style / nav / footer blocks
    html = re.sub(r"<(script|style|nav|footer|header|aside)[^>]*>.*?</\1>",
                  "", html, flags=re.DOTALL | re.IGNORECASE)
    # Remove remaining tags
    text = re.sub(r"<[^>]+>", " ", html)
    # Decode common entities
    text = (text.replace("&amp;", "&").replace("&lt;", "<")
                .replace("&gt;", ">").replace("&quot;", '"')
                .replace("&#39;", "'").replace("&nbsp;", " "))
    # Collapse whitespace
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return "\n".join(lines)


# ── Smart Search Dispatcher ───────────────────────────────────────────────────

CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)

EXPLOIT_KEYWORDS = frozenset([
    "exploit", "poc", "payload", "rce", "lfi", "sqli", "xss", "ssrf",
    "bypass", "injection", "overflow", "shellcode", "metasploit", "msfvenom",
])

FIX_KEYWORDS = frozenset([
    "fix", "patch", "mitigate", "harden", "secure", "remediate",
    "update", "upgrade", "configuration", "防御",
])


def handle_search_dispatch(query: str) -> str:
    """
    Called by the agentic loop when LLM writes [SEARCH: something].
    Routes to the most appropriate search function.

    Priority order:
      1. CVE ID detected → CVE lookup
      2. Exploit keywords → exploit search
      3. Fix/patch keywords → fix search
      4. Default → general web search
    """
    query = query.strip()
    log.info("Search dispatch: %s", query[:80])

    cve_match = CVE_RE.search(query)
    if cve_match:
        return search_cve(cve_match.group())

    q_lower = query.lower()
    if any(kw in q_lower for kw in EXPLOIT_KEYWORDS):
        return web_search(query + " exploit poc github site:github.com OR site:exploit-db.com", max_results=5)

    if any(kw in q_lower for kw in FIX_KEYWORDS):
        return search_fix(query)

    return web_search(query, max_results=5)
