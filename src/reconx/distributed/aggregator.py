import logging

logger = logging.getLogger("reconx")

class CentralAggregator:
    def __init__(self):
        self.global_nodes = set()
        self.global_edges = set()
        self.findings_count = 0

    async def process_worker_data(self, data: dict):
        target = data.get("target")
        results = data.get("results", [])
        
        for result in results:
            self.global_nodes.add(target)
            self.global_nodes.add(result)
            self.global_edges.add(f"{target} -> {result}")
            self.findings_count += 1
            
        logger.info(f"[AGGREGATOR] Processed {len(results)} findings for {target}. Total Global Nodes: {len(self.global_nodes)}")

    def export_graph(self):
        return {
            "nodes": list(self.global_nodes),
            "edges": list(self.global_edges)
        }
