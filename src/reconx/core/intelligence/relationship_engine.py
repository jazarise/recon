from typing import Dict, Any, List


class RelationshipEngine:
    @staticmethod
    def infer_parent_child(assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        relationships = []
        # Group by value for easy lookup
        # In a real scenario, this would query DB, but we do it in memory for ingested batch

        domains = [a for a in assets if a.get("asset_type") == "DOMAIN"]
        subdomains = [a for a in assets if a.get("asset_type") == "SUBDOMAIN"]

        # very simplified inference
        for sub in subdomains:
            sub_val = sub.get("value", "")
            for dom in domains:
                dom_val = dom.get("value", "")
                if sub_val.endswith(f".{dom_val}"):
                    relationships.append(
                        {
                            "parent_value": dom_val,
                            "child_value": sub_val,
                            "relationship_type": "subdomain_of",
                        }
                    )
                    break
        return relationships
