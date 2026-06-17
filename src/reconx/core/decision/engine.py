from reconx.core.strategy.optimizer import strategy_optimizer


class DecisionEngine:
    """The Autonomous Brain that dictates the next optimal move."""

    def decide_next_action(self, target: str) -> str:
        # Queries the Strategy Optimizer for the mathematically optimal capability
        best_capability = strategy_optimizer.get_highest_yield_capability()
        print(f"\n[DECISION ENGINE] Analyzing optimum scan vector for {target}...")
        print(
            f"  -> Selected Strategy: '{best_capability}' (Highest Yield Score: {strategy_optimizer.capability_weights[best_capability]:.2f})"
        )
        return best_capability


decision_engine = DecisionEngine()
