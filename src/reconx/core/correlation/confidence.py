from typing import List
from core.models import Asset

class ConfidenceScorer:
    """Applies heuristic scoring formulas to rate the reliability of an Asset."""

    # Pre-defined confidence multipliers based on source tools
    SOURCE_CONFIDENCE = {
        "amass": 0.95,
        "subfinder": 0.90,
        "assetfinder": 0.85,
        "katana": 0.95,
        "nuclei": 0.99,
        "dalfox": 0.95,
        "mapper_inference": 0.70
    }

    def score(self, assets: List[Asset]) -> List[Asset]:
        for asset in assets:
            base = 0.5
            
            # If we merged multiple sources in Deduplicator, the source field is comma-separated
            sources = asset.source.split(",")
            best_source_score = 0.0
            
            for s in sources:
                best_source_score = max(best_source_score, self.SOURCE_CONFIDENCE.get(s.strip(), base))
                
            # If multiple sources corroborated this, boost confidence
            if len(sources) > 1:
                best_source_score = min(1.0, best_source_score + (0.05 * len(sources)))
                
            asset.confidence = round(best_source_score, 2)
            
        return assets
