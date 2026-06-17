from typing import List, Dict, Any


class Deduplicator:
    @staticmethod
    def deduplicate_assets(assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        deduped = []
        for asset in assets:
            # Assumes assets have been normalized
            key = f"{asset.get('asset_type')}:{asset.get('value')}"
            if key not in seen:
                seen.add(key)
                deduped.append(asset)
        return deduped

    @staticmethod
    def deduplicate_findings(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        deduped = []
        for finding in findings:
            key = f"{finding.get('title')}:{finding.get('severity')}:{finding.get('asset_value', '')}"
            if key not in seen:
                seen.add(key)
                deduped.append(finding)
        return deduped
