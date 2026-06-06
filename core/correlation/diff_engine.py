from typing import List, Dict
from core.models import Asset

class DiffEngine:
    """Calculates differences between two asset sets (e.g. historical vs current scans)."""

    def _hash_assets(self, assets: List[Asset]) -> Dict[str, Asset]:
        # Hash by type and value
        return {f"{a.type.value}::{a.value.lower()}": a for a in assets}

    def diff(self, previous: List[Asset], current: List[Asset]) -> Dict[str, List[Asset]]:
        prev_map = self._hash_assets(previous)
        curr_map = self._hash_assets(current)

        new_assets = []
        removed_assets = []
        unchanged_assets = []

        for hsh, asset in curr_map.items():
            if hsh not in prev_map:
                new_assets.append(asset)
            else:
                unchanged_assets.append(asset)

        for hsh, asset in prev_map.items():
            if hsh not in curr_map:
                removed_assets.append(asset)

        return {
            "new": new_assets,
            "removed": removed_assets,
            "unchanged": unchanged_assets
        }
