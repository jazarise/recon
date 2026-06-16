from typing import List, Dict
from reconx.core.models.enums import AssetType

class AttackPathfinder:
    """Traverses the correlation graph to identify likely exploitation chains."""
    
    def generate_paths(self, assets: List, relationships: List) -> List[Dict]:
        paths = []
        
        # O(N) lookup index
        asset_map = {a.id: a for a in assets}
        
        # In a real graph DB (Neo4j), this is a Cypher query:
        # MATCH (d:DOMAIN)-[:EXPOSES]->(a:API_ENDPOINT) WHERE NOT (a)-[:USES]->(:AUTH_METHOD)
        
        # Here we use Python heuristics to find structural weaknesses
        for asset in assets:
            if asset.type == AssetType.API_ENDPOINT:
                # Find if it has an AUTH_METHOD
                auth_rels = [r for r in relationships if r.source_id == asset.id and asset_map[r.target_id].type == AssetType.AUTH_METHOD]
                
                # If no auth relation exists, or auth is explicitly PUBLIC, it's a weak point
                is_public = True
                if auth_rels:
                    auth_node = asset_map[auth_rels[0].target_id]
                    if auth_node.value != "PUBLIC":
                        is_public = False
                        
                if is_public:
                    paths.append({
                        "path_id": f"path_{asset.id}",
                        "entry_node": asset,
                        "vulnerability": "Missing Authentication",
                        "impact": "Direct Unauthorized Access",
                        "severity": "HIGH" if "admin" in asset.value else "MEDIUM"
                    })
                    
            elif asset.type == AssetType.SECRET:
                paths.append({
                    "path_id": f"path_{asset.id}",
                    "entry_node": asset,
                    "vulnerability": "Hardcoded Credential Exposure",
                    "impact": "Account Takeover / Cloud Compromise",
                    "severity": "CRITICAL"
                })
                
        return paths

pathfinder = AttackPathfinder()
