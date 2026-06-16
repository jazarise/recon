class GraphPruner:
    @staticmethod
    def compress_graph(nodes: list, scores: dict) -> list:
        # Aggressively strip low value nodes
        compressed = []
        for node in nodes:
            if scores.get(node, {}).get("total_score", 0) > 0.3:
                compressed.append(node)
        return compressed
