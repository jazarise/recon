import asyncio
from core.plugin_interface import PluginInterface

class ToolAdapter(PluginInterface):
    async def execute(self, config: dict, context: dict) -> dict:
        target = context.get("target", "unknown")
        findings = context.get("findings", [])
        
        # In a real environment, we would send 'findings' to an LLM via API.
        # Here we simulate the LLM inference based on rule logic on the collected context.
        await asyncio.sleep(1.0)
        
        open_ports = []
        technologies = []
        ips = []
        
        if "network_discovery" in context and context["network_discovery"]:
            open_ports = context["network_discovery"].get("open_ports", [])
            
        if "web_recon" in context and context["web_recon"]:
            technologies = context["web_recon"].get("technologies", [])
            
        if "dns_intelligence" in context and context["dns_intelligence"]:
            records = context["dns_intelligence"].get("records", {})
            ips = records.get("A", [])

        risk_score = 0
        recommendations = []
        
        if 80 in open_ports and 443 not in open_ports:
            risk_score += 30
            recommendations.append("Enforce HTTPS on port 443; port 80 is currently exposed without secure alternative.")
            
        if "Unknown" in technologies:
            recommendations.append("Web server technology could not be fingerprinted. Ensure headers are stripped securely.")
            
        if not ips:
            risk_score += 10
            recommendations.append("No A records resolved for the target domain.")
            
        if risk_score == 0:
            risk_score = 10
            recommendations.append("No critical misconfigurations found. Continue regular monitoring.")

        summary = (
            f"LLM Analysis for {target}: Analyzed {len(findings)} raw findings. "
            f"Detected {len(open_ports)} open ports and {len(technologies)} web technologies. "
            f"Calculated risk score is {risk_score}/100."
        )

        return {
            "plugin": "llm_analysis",
            "summary": summary,
            "recommendations": recommendations,
            "risk_score": risk_score
        }
