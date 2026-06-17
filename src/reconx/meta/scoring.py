class QualityScorer:
    @staticmethod
    def evaluate_node(asset: str, source: str) -> dict:
        relevance = 0.9 if "api" in asset or "admin" in asset else 0.4
        novelty = 1.0  # Simulated novelty
        risk = 0.8 if "api" in asset else 0.2
        confidence = 0.95 if source == "active_dns" else 0.5

        return {
            "asset": asset,
            "relevance": relevance,
            "novelty": novelty,
            "risk": risk,
            "confidence": confidence,
            "total_score": (relevance + risk + confidence) / 3,
        }
