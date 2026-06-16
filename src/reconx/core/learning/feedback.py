from core.strategy.optimizer import strategy_optimizer

class LearningEngine:
    """Evaluates scan results and translates them into strategy weight changes."""
    
    def evaluate_scan(self, capability: str, target: str, new_assets_found: int, duration_sec: float):
        print(f"[LEARNING] Evaluating scan: {capability} on {target}")
        
        # Heuristic scoring
        if new_assets_found == 0:
            # Penalize the capability for finding nothing
            penalty = -2.0
            print(f"  -> Found 0 assets in {duration_sec}s. Decreasing priority.")
            strategy_optimizer.adjust_weight(capability, penalty)
        else:
            # Reward the capability based on yield density
            yield_score = (new_assets_found / max(1.0, duration_sec)) * 5.0
            print(f"  -> Found {new_assets_found} assets in {duration_sec}s. Increasing priority by {yield_score:.2f}.")
            strategy_optimizer.adjust_weight(capability, yield_score)

learning_engine = LearningEngine()
