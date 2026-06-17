from typing import Dict, Any, List


class AssetGraph:
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, str]] = []

    def add_node(self, asset_value: str, properties: Dict[str, Any]):
        self.nodes[asset_value] = properties

    def add_edge(self, parent_value: str, child_value: str, rel_type: str):
        if parent_value in self.nodes and child_value in self.nodes:
            self.edges.append(
                {"source": parent_value, "target": child_value, "type": rel_type}
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [{"id": k, **v} for k, v in self.nodes.items()],
            "edges": self.edges,
        }
