import logging
from typing import List, Dict, Any

logger = logging.getLogger("reconx.diffing")

class AssetDiffer:
    """Native continuous diffing logic ported from ScopeSentry."""
    
    @staticmethod
    def diff_assets(old_assets: List[Dict[str, Any]], new_assets: List[Dict[str, Any]], key_field: str = "value") -> Dict[str, List[Dict[str, Any]]]:
        """Compares two asset lists and returns new, removed, and common assets."""
        old_map = {a.get(key_field): a for a in old_assets if a.get(key_field)}
        new_map = {a.get(key_field): a for a in new_assets if a.get(key_field)}
        
        added = []
        removed = []
        common = []
        
        for k, v in new_map.items():
            if k not in old_map:
                added.append(v)
            else:
                common.append(v)
                
        for k, v in old_map.items():
            if k not in new_map:
                removed.append(v)
                
        logger.info(f"Diff complete. Added: {len(added)}, Removed: {len(removed)}, Common: {len(common)}")
        
        return {
            "added": added,
            "removed": removed,
            "common": common
        }

    @staticmethod
    def generate_alerts(diff_result: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Generates findings/alerts for newly discovered assets."""
        alerts = []
        for asset in diff_result.get("added", []):
            alerts.append({
                "type": "new_asset_discovered",
                "severity": "info",
                "title": f"New Asset Discovered: {asset.get('value', 'Unknown')}",
                "description": f"A new {asset.get('type', 'asset')} was discovered during continuous monitoring.",
                "tags": ["scopesentry", "diffing", "continuous_monitoring"]
            })
        return alerts
