from typing import List, Dict, Any
from core.models import Asset, Relationship, Finding

class GraphBuilder:
    """Transforms unified models into a structured Node/Edge graph suitable for visualization and AI."""

    def build_graph(self, assets: List[Asset], relationships: List[Relationship], findings: List[Finding]) -> Dict[str, Any]:
        nodes = []
        edges = []

        # Assets as nodes
        for asset in assets:
            nodes.append({
                "id": asset.id,
                "label": asset.value,
                "type": asset.type.value,
                "confidence": asset.confidence,
                "group": "asset"
            })

        # Findings as nodes
        for finding in findings:
            finding_node_id = f"finding_{finding.id}"
            nodes.append({
                "id": finding_node_id,
                "label": finding.title,
                "type": "FINDING",
                "severity": finding.severity.value,
                "group": "finding"
            })
            
            # Implicit edge from asset to finding
            if finding.asset_id:
                edges.append({
                    "source": finding.asset_id,
                    "target": finding_node_id,
                    "label": "AFFECTED_BY"
                })

        # Relationships as edges
        for rel in relationships:
            edges.append({
                "source": rel.source_id,
                "target": rel.target_id,
                "label": rel.type.value
            })

        # Basic stats
        stats = {
            "assets": len(assets),
            "findings": len(findings),
            "relationships": len(edges)
        }

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": stats
        }
