from typing import List, Dict
from core.models import Asset

class Deduplicator:
    """Normalizes and deduplicates assets."""

    @staticmethod
    def _get_signature(asset: Asset) -> str:
        """Generate a unique signature for an asset to identify duplicates."""
        # Normalize the value
        val = asset.value.lower().strip()
        
        if asset.type.value in ["DOMAIN", "SUBDOMAIN"]:
            # remove trailing dots or http/https if accidentally included
            val = val.replace("https://", "").replace("http://", "").rstrip("/")
            
        return f"{asset.type.value}::{val}"

    def deduplicate(self, assets: List[Asset]) -> List[Asset]:
        """
        Takes a list of raw assets and squashes duplicates based on signature.
        Combines sources and tags into the canonical asset.
        """
        seen: Dict[str, Asset] = {}
        
        for asset in assets:
            sig = self._get_signature(asset)
            if sig in seen:
                # Merge logic
                canonical = seen[sig]
                
                # Combine tags
                canonical.tags = list(set(canonical.tags + asset.tags))
                
                # We could append sources to a list if we change the Asset model, 
                # but for now we'll just keep the first source or mark it as 'multiple'
                if canonical.source != asset.source and "multiple" not in canonical.source:
                    canonical.source = f"{canonical.source},{asset.source}"
                    
                # Take highest confidence
                canonical.confidence = max(canonical.confidence, asset.confidence)
            else:
                seen[sig] = asset
                
        return list(seen.values())
