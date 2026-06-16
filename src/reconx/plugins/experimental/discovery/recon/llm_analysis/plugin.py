from core.plugin_base import standardize_output
def setup_logger(*args, **kwargs): pass
from core.http.client import HttpClient
"""
ReconX LLM Analysis Plugin — AI-powered attack surface analysis.
Uses OpenAI when available; falls back to rule-based local analysis
so scans always complete regardless of API key availability.
"""

import os
import json
import re
from datetime import datetime, timezone



logger = setup_logger("llm_analysis")

# Risk score weights
RISK_WEIGHTS = {
    "open_port_21": 20,   # FTP
    "open_port_22": 10,   # SSH
    "open_port_23": 35,   # Telnet
    "open_port_80": 5,
    "open_port_443": 0,
    "open_port_445": 40,  # SMB
    "open_port_3306": 30, # MySQL
    "open_port_5432": 25, # Postgres
    "open_port_6379": 35, # Redis (unauthenticated risk)
    "open_port_27017": 35,# MongoDB
    "open_port_9200": 35, # Elasticsearch
    "open_port_8080": 10,
    "open_port_8443": 5,
    "dns_cname": 5,
    "web_service": 5,
}

HIGH_RISK_PORTS = {21, 23, 445, 6379, 9200, 27017}
MED_RISK_PORTS  = {22, 3306, 5432, 1433, 5900, 8080}


class Plugin:
    name = 'llm_analysis'
    category = 'recon'
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target   = context.get("target", "unknown")
        api_key  = os.getenv("OPENAI_API_KEY", "")

        # Gather context from previous steps
        nd  = context.get("network_discovery", {}) or {}
        wr  = context.get("web_recon", {}) or {}
        dns = context.get("dns_intelligence", {}) or {}

        open_ports   = nd.get("open_ports", [])
        urls         = wr.get("urls", [])
        technologies = wr.get("technologies", [])
        dns_records  = dns.get("records", {})
        findings     = context.get("findings", [])

        summary_data = {
            "target":        target,
            "open_ports":    open_ports,
            "urls":          urls,
            "technologies":  technologies,
            "dns_records":   dns_records,
            "total_findings": len(findings),
        }

        if api_key:
            result = await self._openai_analysis(api_key, target, summary_data)
            if result:
                return result

        # Fallback — rule-based local analysis
        return self._rule_based_analysis(target, open_ports, technologies, dns_records, urls)

    # ── OpenAI path ──────────────────────────────────────────────────────

    async def _openai_analysis(self, api_key: str, target: str, data: dict) -> dict | None:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=api_key)

            prompt = f"""Analyze the following reconnaissance data for '{target}' and return a JSON object with these fields:
{{
  "executive_summary": "2-3 sentence professional summary",
  "risk_score": <integer 0-100>,
  "risk_level": "<CRITICAL|HIGH|MEDIUM|LOW|MINIMAL>",
  "key_findings": ["..."],
  "recommendations": ["..."],
  "attack_vectors": ["..."]
}}

Recon data:
{json.dumps(data, indent=2)}

Respond ONLY with valid JSON — no markdown, no explanation."""

            resp = await client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a senior penetration tester. Output only valid JSON."},
                    {"role": "user",   "content": prompt},
                ],
                response_format={"type": "json_object"},
                max_tokens=800,
            )
            result = json.loads(resp.choices[0].message.content)
            result["source"] = "openai"
            result["plugin"] = "llm_analysis"
            result["findings"] = []
            return result
        except Exception as e:
            logger.warning(f"OpenAI analysis failed: {e} — falling back to rule-based analysis")
            return None

    # ── Rule-based fallback ──────────────────────────────────────────────

    def _rule_based_analysis(
        self,
        target: str,
        open_ports: list,
        technologies: list,
        dns_records: dict,
        urls: list,
    ) -> dict:
        score = 0
        key_findings     = []
        recommendations  = []
        attack_vectors   = []

        port_set = set(open_ports)

        # Score open ports
        for port in port_set:
            score += RISK_WEIGHTS.get(f"open_port_{port}", 3)
            if port in HIGH_RISK_PORTS:
                key_findings.append(f"High-risk service detected on port {port}")
            elif port in MED_RISK_PORTS:
                key_findings.append(f"Sensitive service detected on port {port}")

        # FTP
        if 21 in port_set:
            attack_vectors.append("FTP brute-force or anonymous login attempt")
            recommendations.append("Disable FTP; use SFTP/FTPS with strong credentials")

        # SSH
        if 22 in port_set:
            attack_vectors.append("SSH credential brute-force or key exploitation")
            recommendations.append("Enforce SSH key-based authentication; disable password login")

        # Telnet
        if 23 in port_set:
            key_findings.append("CRITICAL: Telnet is enabled (cleartext protocol)")
            attack_vectors.append("Cleartext credential interception via Telnet")
            recommendations.append("Immediately disable Telnet and replace with SSH")

        # SMB
        if 445 in port_set:
            key_findings.append("SMB port open — potential EternalBlue exposure")
            attack_vectors.append("SMB exploitation (EternalBlue / lateral movement)")
            recommendations.append("Patch SMB, disable SMBv1, restrict SMB to internal subnets")

        # Database ports
        for db_port, db_name in [(3306, "MySQL"), (5432, "PostgreSQL"), (1433, "MSSQL"),
                                  (27017, "MongoDB"), (6379, "Redis"), (9200, "Elasticsearch")]:
            if db_port in port_set:
                key_findings.append(f"{db_name} port {db_port} exposed — verify access controls")
                attack_vectors.append(f"Unauthenticated {db_name} access or credential stuffing")
                recommendations.append(f"Restrict {db_name} port to trusted hosts; enforce authentication")

        # Web services
        web_ports = {80, 443, 8080, 8443}
        if port_set & web_ports:
            attack_vectors.append("Web application enumeration and vulnerability scanning")
            recommendations.append("Run authenticated web application scan (e.g., Nuclei, Nikto)")

        # Technologies
        for tech in technologies:
            tech_l = tech.lower()
            if any(x in tech_l for x in ["apache", "nginx", "iis"]):
                recommendations.append(f"Ensure {tech} is patched to the latest stable version")
            if "php" in tech_l:
                attack_vectors.append("PHP-based code injection or deserialization attacks")

        # DNS
        if dns_records.get("CNAME"):
            attack_vectors.append("Subdomain takeover via dangling CNAME records")
            recommendations.append("Audit CNAME records for dangling/unclaimed third-party targets")

        # Clamp score
        score = min(score, 100)

        if score >= 70:
            risk_level = "CRITICAL"
        elif score >= 50:
            risk_level = "HIGH"
        elif score >= 30:
            risk_level = "MEDIUM"
        elif score >= 10:
            risk_level = "LOW"
        else:
            risk_level = "MINIMAL"

        port_summary = f"{len(port_set)} open port(s)" if port_set else "no open ports detected"
        tech_summary = f"Technologies: {', '.join(technologies[:3])}" if technologies else ""

        summary = (
            f"Reconnaissance of {target} identified {port_summary}. "
            f"{tech_summary + '. ' if tech_summary else ''}"
            f"Rule-based risk assessment produced a score of {score}/100 ({risk_level})."
        )

        if not key_findings:
            key_findings.append("No critical exposures detected in basic scan")
        if not recommendations:
            recommendations.append("Conduct a deeper scan to identify application-layer vulnerabilities")

        return {
            "plugin":           "llm_analysis",
            "source":           "rule_based",
            "target":           target,
            "risk_score":       score,
            "risk_level":       risk_level,
            "executive_summary": summary,
            "key_findings":     key_findings,
            "recommendations":  recommendations,
            "attack_vectors":   attack_vectors,
            "summary":          summary,
            "findings":         [],
            "generated_at":     datetime.now(timezone.utc).isoformat() + "Z",
        }

# Auto-injected Metadata
PLUGIN_NAME = "llm_analysis"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for llm_analysis"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = []
