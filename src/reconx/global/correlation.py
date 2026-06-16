from src.reconx.global.graph import NetworkGraph

class CorrelationEngine:
    def __init__(self):
        self.graph = NetworkGraph()
        
    def ingest_tenant_data(self, tenant_id: str, data: dict):
        # Map infrastructure to find cross-tenant overlap
        ip = data.get("ip")
        domain = data.get("domain")
        if ip and domain:
            self.graph.add_relationship(ip, domain)

    def generate_heatmap(self) -> dict:
        return {
            "critical_clusters": len(self.graph.edges),
            "status": "Global Risk Map Updated"
        }
