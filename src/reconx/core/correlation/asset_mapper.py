import re
from typing import List
from reconx.core.models import Asset, AssetType
from reconx.core.normalization import AssetNormalizer

class AssetMapper:
    """Extracts implicit assets from explicit ones (e.g., extracting IP from a URL string)."""

    def map_implicit_assets(self, assets: List[Asset]) -> List[Asset]:
        implicit = []
        ip_regex = re.compile(r"(\d{1,3}\.){3}\d{1,3}")
        
        for asset in assets:
            if asset.type == AssetType.URL:
                # If URL contains an IP instead of domain
                match = ip_regex.search(asset.value)
                if match:
                    implicit.append(AssetNormalizer.create_ip(match.group(0), source="mapper_inference"))
        return implicit
