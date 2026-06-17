import os
import json
import asyncio
from datetime import datetime
from core.plugin_interface import PluginInterface

class ToolAdapter(PluginInterface):
    async def execute(self, config: dict, context: dict) -> dict:
        target = context.get("target", "unknown")
        
        # Build report
        report_lines = [
            f"# ReconX Intelligence Report: {target}",
            f"Generated: {datetime.utcnow().isoformat()}Z\n",
            "## 1. Network Discovery",
        ]
        
        nd = context.get("network_discovery", {})
        if nd:
            report_lines.append(f"- Open Ports: {', '.join(map(str, nd.get('open_ports', [])))}")
        else:
            report_lines.append("- No network data available.")
            
        report_lines.append("\n## 2. Web Reconnaissance")
        wr = context.get("web_recon", {})
        if wr:
            report_lines.append(f"- URLs found: {len(wr.get('urls', []))}")
            report_lines.append(f"- Technologies: {', '.join(wr.get('technologies', []))}")
        else:
            report_lines.append("- No web data available.")
            
        report_lines.append("\n## 3. DNS Intelligence")
        dns = context.get("dns_intelligence", {})
        if dns:
            records = dns.get("records", {})
            for rtype, rdata in records.items():
                report_lines.append(f"- {rtype}: {', '.join(rdata)}")
        else:
            report_lines.append("- No DNS data available.")
            
        report_lines.append("\n## 4. LLM Analysis & Recommendations")
        llm = context.get("llm_analysis", {})
        if llm:
            report_lines.append(f"**Risk Score:** {llm.get('risk_score', 'N/A')}/100\n")
            report_lines.append(f"**Summary:** {llm.get('summary', 'N/A')}\n")
            report_lines.append("**Recommendations:**")
            for rec in llm.get('recommendations', []):
                report_lines.append(f"- {rec}")
        else:
            report_lines.append("- No LLM analysis available.")

        # Save report
        outputs_dir = "e:/ReconX/outputs"
        os.makedirs(outputs_dir, exist_ok=True)
        report_name = f"report_{target.replace('.', '_')}_{int(datetime.utcnow().timestamp())}.md"
        report_path = os.path.join(outputs_dir, report_name)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        return {
            "plugin": "reporting",
            "report_path": report_path,
            "report_type": "Markdown"
        }
