from core.plugin_manager.interface import ReconXPlugin
from core.engine.correlation_engine import CorrelationEngine
import json
import os

class ReportingPlugin(ReconXPlugin):
    name = "reporting"
    version = "3.0.0"
    description = "Generate OSINT enhanced JSON, HTML, and Markdown reports"

    def run(self, target: str, **kwargs):
        context = kwargs.get('context', {})
        results = context.get('all_results', [])
        
        engine = CorrelationEngine()
        engine.ingest(results, org_name=target)
        profiles = engine.get_profiles()
        
        report_data = [p.model_dump() for p in profiles]
        
        os.makedirs("reports", exist_ok=True)
        with open("reports/osint_report.json", "w") as f:
            json.dump(report_data, f, indent=4)
            
        with open("reports/osint_report.md", "w") as f:
            f.write(f"# ReconX Intelligence Report for {target}\n")
            for p in profiles:
                f.write(f"## Organization: {p.organization}\n")
                f.write(f"### Emails Discovered: {len(p.emails)}\n")
                for e in p.emails:
                    f.write(f"- {e.value} (Confidence: {e.confidence.value})\n")
                f.write(f"\n### Social Profiles Discovered: {len(p.social_profiles)}\n")
                for s in p.social_profiles:
                    f.write(f"- {s.platform}: {s.username} ({s.url})\n")
                f.write(f"\n### Breach Records: {len(p.breach_records)}\n")
                for b in p.breach_records:
                    f.write(f"- Source: {b.source} (Type: {b.exposure_type})\n")
                f.write(f"\n### Threat Indicators: {len(p.threat_indicators)}\n")
                for t in p.threat_indicators:
                    f.write(f"- {t.indicator_type.upper()}: {t.value}\n")
                f.write("\n---\n")
                
        with open("reports/osint_report.html", "w") as f:
            f.write(f"<html><body><h1>ReconX Intelligence Report for {target}</h1></body></html>")
            
        return {"report_path": "reports/osint_report.json"}
