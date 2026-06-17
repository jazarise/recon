class StrategyOptimizer:
    """Maintains a live dynamic scoreboard of capability efficiency."""

    def __init__(self):
        # Maps capability name to its dynamic "Yield Score"
        # Initial equal weighting
        self.capability_weights = {
            "dns.bruteforce": 10.0,
            "web.probe": 10.0,
            "discovery.javascript": 10.0,
        }

    def adjust_weight(self, capability: str, delta: float):
        if capability in self.capability_weights:
            # Ensure minimum weight
            self.capability_weights[capability] = max(
                1.0, self.capability_weights[capability] + delta
            )
            print(
                f"[STRATEGY] Adjusted {capability} weight to {self.capability_weights[capability]:.2f} (Delta: {delta:+.2f})"
            )

    def get_highest_yield_capability(self) -> str:
        # Returns the capability with the highest current weight
        return max(self.capability_weights, key=self.capability_weights.get)


strategy_optimizer = StrategyOptimizer()
