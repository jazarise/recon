"""
ReconX Reporting Plugin — generates MD, JSON, CSV, and HTML reports
from correlated workflow context data.
"""

import csv
import json
import os
from datetime import datetime
from pathlib import Path

from core.plugin_interface import PluginInterface

OUTPUTS_DIR = Path(__file__).resolve().parent.parent.parent / "outputs"


def _escape(s: str) -> str:
    return (str(s)
            .replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


class ToolAdapter(PluginInterface):
    async def execute(self, config: dict, context: dict) -> dict:
        target    = context.get("target", "unknown")
        nd        = context.get("network_discovery", {}) or {}
        wr        = context.get("web_recon", {}) or {}
        dns       = context.get("dns_intelligence", {}) or {}
        llm       = context.get("llm_analysis", {}) or {}
        findings  = context.get("findings", [])

        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

        ts         = int(datetime.utcnow().timestamp())
        safe_tgt   = target.replace(".", "_").replace("/", "_").replace(":", "_")
        base       = OUTPUTS_DIR / f"report_{safe_tgt}_{ts}"

        md_path   = self._write_markdown(base, target, nd, wr, dns, llm, findings)
        json_path = self._write_json(base, target, nd, wr, dns, llm, findings)
        csv_path  = self._write_csv(base, nd, wr, dns)
        html_path = self._write_html(base, target, nd, wr, dns, llm, findings)

        return {
            "plugin":      "reporting",
            "target":      target,
            "reports": {
                "markdown": str(md_path),
                "json":     str(json_path),
                "csv":      str(csv_path),
                "html":     str(html_path),
            },
            "report_path": str(html_path),
            "findings":    [],
        }

    # ── Markdown ─────────────────────────────────────────────────────────

    def _write_markdown(self, base, target, nd, wr, dns, llm, findings) -> Path:
        ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        lines = [
            f"# ReconX Intelligence Report — {target}",
            f"> Generated: {ts}",
            "",
            "---",
            "",
        ]
        risk_score = llm.get("risk_score", "N/A")
        risk_level = llm.get("risk_level", "UNKNOWN")
        lines += [
            f"## Executive Summary",
            "",
            llm.get("executive_summary") or llm.get("summary") or "_No LLM analysis available._",
            "",
            f"**Risk Score:** {risk_score}/100  **Risk Level:** {risk_level}",
            "",
            "---",
            "",
            "## Network Discovery",
            "",
        ]
        open_ports = nd.get("open_ports", [])
        if open_ports:
            lines.append(f"Open ports: `{', '.join(map(str, open_ports))}`")
            for svc in nd.get("services", []):
                port  = svc.get("port", "?")
                state = svc.get("state", "?")
                lines.append(f"- Port **{port}** — {state}")
        else:
            lines.append("_No open ports detected._")

        lines += ["", "## DNS Intelligence", ""]
        records = dns.get("records", {})
        if records:
            for rtype, vals in records.items():
                lines.append(f"**{rtype}**: {', '.join(vals)}")
        else:
            lines.append("_No DNS records found._")

        lines += ["", "## Web Reconnaissance", ""]
        urls = wr.get("urls", [])
        techs = wr.get("technologies", [])
        if urls:
            for u in urls:
                lines.append(f"- `{u}`")
        if techs:
            lines.append(f"\nTechnologies: {', '.join(techs)}")
        if not urls:
            lines.append("_No web services detected._")

        lines += ["", "## Key Findings", ""]
        for f in llm.get("key_findings", []):
            lines.append(f"- {f}")
        if not llm.get("key_findings"):
            lines.append("_No key findings._")

        lines += ["", "## Recommendations", ""]
        for r in llm.get("recommendations", []):
            lines.append(f"- {r}")

        path = Path(str(base) + ".md")
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    # ── JSON ──────────────────────────────────────────────────────────────

    def _write_json(self, base, target, nd, wr, dns, llm, findings) -> Path:
        data = {
            "meta": {
                "tool":         "ReconX",
                "version":      "1.0.0",
                "target":       target,
                "generated_at": datetime.utcnow().isoformat() + "Z",
            },
            "network_discovery": nd,
            "web_recon":         wr,
            "dns_intelligence":  dns,
            "llm_analysis":      llm,
            "findings":          findings,
        }
        path = Path(str(base) + ".json")
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        return path

    # ── CSV ───────────────────────────────────────────────────────────────

    def _write_csv(self, base, nd, wr, dns) -> Path:
        path = Path(str(base) + ".csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Category", "Key", "Value"])
            for p in nd.get("open_ports", []):
                w.writerow(["Network", "open_port", str(p)])
            for svc in nd.get("services", []):
                w.writerow(["Network", "service", f"port={svc.get('port')} state={svc.get('state')}"])
            for u in wr.get("urls", []):
                w.writerow(["Web", "url", u])
            for t in wr.get("technologies", []):
                w.writerow(["Web", "technology", t])
            for rtype, vals in dns.get("records", {}).items():
                for v in (vals if isinstance(vals, list) else [vals]):
                    w.writerow(["DNS", rtype, v])
        return path

    # ── HTML ──────────────────────────────────────────────────────────────

    def _write_html(self, base, target, nd, wr, dns, llm, findings) -> Path:
        ts         = datetime.utcnow().strftime("%B %d, %Y  %H:%M:%S UTC")
        risk_score = llm.get("risk_score", 0) or 0
        risk_level = llm.get("risk_level", "UNKNOWN")
        summary    = _escape(llm.get("executive_summary") or llm.get("summary") or "No analysis available.")
        open_ports = nd.get("open_ports", [])
        urls       = wr.get("urls", [])
        technologies = wr.get("technologies", [])
        records    = dns.get("records", {})
        key_findings    = llm.get("key_findings", [])
        recommendations = llm.get("recommendations", [])
        attack_vectors  = llm.get("attack_vectors", [])
        source     = llm.get("source", "rule_based")

        risk_color = {
            "CRITICAL": "#ff2d55", "HIGH": "#ff6b35",
            "MEDIUM": "#ffd60a",   "LOW": "#30d158", "MINIMAL": "#636366",
        }.get(risk_level, "#636366")

        def rows_port(services):
            if not services:
                return '<tr><td colspan="2" class="empty">No services detected</td></tr>'
            out = ""
            for svc in services:
                port  = _escape(str(svc.get("port", "?")))
                state = _escape(svc.get("state", "unknown"))
                badge = "badge-open" if state == "open" else "badge-dim"
                out += f'<tr><td class="mono">{port}</td><td><span class="badge {badge}">{state}</span></td></tr>'
            return out

        services_rows = rows_port(nd.get("services", []))

        def li_list(items):
            if not items:
                return '<li class="empty">None identified</li>'
            return "".join(f"<li>{_escape(str(i))}</li>" for i in items)

        dns_section = ""
        for rtype, vals in records.items():
            vals_str = ", ".join(vals) if isinstance(vals, list) else str(vals)
            dns_section += f'<tr><td class="mono">{_escape(rtype)}</td><td class="mono">{_escape(vals_str)}</td></tr>'
        if not dns_section:
            dns_section = '<tr><td colspan="2" class="empty">No DNS records retrieved</td></tr>'

        tech_badges = "".join(f'<span class="tech-badge">{_escape(t)}</span>' for t in technologies)
        url_rows = "".join(f'<tr><td class="mono">{_escape(u)}</td></tr>' for u in urls)
        if not url_rows:
            url_rows = '<tr><td class="empty">No web services detected</td></tr>'

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>ReconX Report — {_escape(target)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Chakra+Petch:wght@400;600;700&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#060a0f;--bg2:#0c1420;--bg3:#111c2d;
  --border:#1a3050;--accent:#e53935;--accent2:#ff6b35;
  --text:#c8d8e8;--dim:#5a7a9a;
  --font:'Chakra Petch',monospace;--mono:'Share Tech Mono',monospace;
  --pass:#30d158;--warn:#ffd60a;--fail:#ff2d55;
}}
html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--text);font-family:var(--font);font-size:14px;line-height:1.6;padding:40px 24px 80px;}}
.container{{max-width:1080px;margin:0 auto}}
.header{{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:20px;border-bottom:1px solid var(--border);padding-bottom:28px;margin-bottom:36px}}
.logo{{font-size:36px;font-weight:700;letter-spacing:6px;color:var(--accent);text-shadow:0 0 24px rgba(229,57,53,.4)}}
.logo-sub{{font-size:12px;color:var(--dim);letter-spacing:2px;margin-top:4px}}
.meta{{text-align:right;font-family:var(--mono);color:var(--dim);font-size:12px;line-height:2}}
.meta .tgt{{color:#64b5f6;font-size:15px;font-weight:600}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:14px;margin-bottom:36px}}
.stat{{background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:18px 14px;text-align:center;transition:border-color .2s}}
.stat:hover{{border-color:var(--accent)}}
.stat-n{{font-size:32px;font-weight:700;font-family:var(--mono);line-height:1;margin-bottom:4px}}
.stat-l{{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--dim)}}
.section{{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:26px;margin-bottom:24px;box-shadow:0 4px 24px rgba(0,0,0,.4)}}
.sec-title{{font-size:13px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--accent);margin-bottom:18px;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--border);padding-bottom:10px}}
.summary-box{{background:var(--bg3);border-left:3px solid var(--accent);border-radius:6px;padding:16px 20px;font-size:13.5px;line-height:1.8;color:var(--text);margin-bottom:16px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--dim);text-align:left;padding:8px 12px;border-bottom:1px solid var(--border)}}
td{{padding:9px 12px;border-bottom:1px solid rgba(26,48,80,.4);vertical-align:top}}
tr:last-child td{{border-bottom:none}}
tr:hover td{{background:rgba(229,57,53,.03)}}
.mono{{font-family:var(--mono);font-size:12px}}
.empty{{color:var(--dim);font-style:italic;padding:16px!important;text-align:center}}
.badge{{display:inline-block;font-size:10px;font-weight:700;letter-spacing:1px;padding:2px 8px;border-radius:4px;text-transform:uppercase}}
.badge-open{{background:rgba(48,209,88,.15);color:var(--pass);border:1px solid rgba(48,209,88,.3)}}
.badge-dim{{background:rgba(100,100,100,.2);color:#888;border:1px solid #444}}
.risk-score{{font-size:40px;font-weight:700;font-family:var(--mono)}}
.tech-badge{{display:inline-block;background:rgba(100,181,246,.1);border:1px solid rgba(100,181,246,.3);color:#64b5f6;font-size:11px;padding:3px 10px;border-radius:20px;margin:3px}}
ul{{list-style:none;padding:0}}
ul li{{padding:6px 0 6px 18px;border-bottom:1px solid rgba(26,48,80,.3);position:relative}}
ul li:last-child{{border-bottom:none}}
ul li::before{{content:"›";position:absolute;left:0;color:var(--accent)}}
ul li.empty{{color:var(--dim);font-style:italic}}
.source-badge{{font-size:9px;background:rgba(229,57,53,.1);border:1px solid rgba(229,57,53,.3);color:var(--accent);padding:2px 8px;border-radius:20px;letter-spacing:1px;margin-left:auto}}
.footer{{text-align:center;margin-top:48px;color:var(--dim);font-size:11px;font-family:var(--mono);border-top:1px solid var(--border);padding-top:24px}}
.footer .disc{{margin-top:6px;font-size:10px;opacity:.55}}
body::after{{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.06) 2px,rgba(0,0,0,.06) 4px);pointer-events:none;z-index:9999}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}
.section{{animation:fadeUp .4s ease both}}
</style>
</head>
<body>
<div class="container">

<header class="header">
  <div>
    <div class="logo">RECONX</div>
    <div class="logo-sub">Unified Reconnaissance Platform · v1.0.0</div>
  </div>
  <div class="meta">
    <div>Generated: {ts}</div>
    <div>Target: <span class="tgt">{_escape(target)}</span></div>
    <div>Source: {_escape(source.replace("_"," ").title())}</div>
  </div>
</header>

<div class="stats">
  <div class="stat">
    <div class="stat-n" style="color:var(--accent2)">{len(open_ports)}</div>
    <div class="stat-l">Open Ports</div>
  </div>
  <div class="stat">
    <div class="stat-n" style="color:#64b5f6">{len(urls)}</div>
    <div class="stat-l">Web Services</div>
  </div>
  <div class="stat">
    <div class="stat-n" style="color:var(--pass)">{len(technologies)}</div>
    <div class="stat-l">Technologies</div>
  </div>
  <div class="stat">
    <div class="stat-n" style="color:{risk_color}">{risk_score}</div>
    <div class="stat-l">Risk Score / 100</div>
  </div>
  <div class="stat">
    <div class="stat-n" style="font-size:18px;color:{risk_color}">{risk_level}</div>
    <div class="stat-l">Risk Level</div>
  </div>
</div>

<div class="section">
  <div class="sec-title">🧠 Executive Summary
    <span class="source-badge">{_escape(source.upper())}</span>
  </div>
  <div class="summary-box">{summary}</div>
  <div style="display:flex;gap:24px;flex-wrap:wrap;margin-top:12px">
    <div><strong>Key Findings</strong><ul>{li_list(key_findings)}</ul></div>
    <div><strong>Attack Vectors</strong><ul>{li_list(attack_vectors)}</ul></div>
  </div>
</div>

<div class="section">
  <div class="sec-title">🛰️ Network Discovery</div>
  <table>
    <thead><tr><th>Port</th><th>State</th></tr></thead>
    <tbody>{services_rows}</tbody>
  </table>
</div>

<div class="section">
  <div class="sec-title">🌐 DNS Intelligence</div>
  <table>
    <thead><tr><th>Record Type</th><th>Values</th></tr></thead>
    <tbody>{dns_section}</tbody>
  </table>
</div>

<div class="section">
  <div class="sec-title">🔍 Web Reconnaissance</div>
  {"<p style='margin-bottom:12px'><strong>Technologies:</strong> " + tech_badges + "</p>" if technologies else ""}
  <table>
    <thead><tr><th>URL</th></tr></thead>
    <tbody>{url_rows}</tbody>
  </table>
</div>

<div class="section">
  <div class="sec-title">🛡️ Recommendations</div>
  <ul>{li_list(recommendations)}</ul>
</div>

<footer class="footer">
  ReconX v1.0.0 · Unified Reconnaissance Platform
  <div class="disc">⚠️ For authorized security testing and educational use only. Do not use against systems you do not own.</div>
</footer>

</div>
</body>
</html>"""

        path = Path(str(base) + ".html")
        path.write_text(html, encoding="utf-8")
        return path
