class AnalysisAgent:
    def evaluate(self, assets_found: int, state) -> str:
        if assets_found > 0:
            return f"Valuable intelligence acquired ({assets_found} new nodes)."
        return "Redundant/Noisy data block. Re-evaluating."
