from core.correlation.rules import deduplicate_findings
from core.correlation.relationships import add_relationship

class CorrelationEngine:
    def process_scan_findings(self, db_session, findings: list):
        deduped = deduplicate_findings(findings)
        
        for f in deduped:
            if f.category == "subdomain":
                add_relationship(db_session, getattr(f, 'source', 'unknown'), "resolves_to", f.value)
            elif f.category == "port":
                add_relationship(db_session, getattr(f, 'source', 'unknown'), "exposes", f"Port {f.value}")
            elif f.category == "vulnerability":
                add_relationship(db_session, getattr(f, 'source', 'unknown'), "affected_by", f.value)
        
        return deduped

correlation_engine = CorrelationEngine()
