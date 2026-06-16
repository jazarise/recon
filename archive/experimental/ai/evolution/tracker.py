import time
from reconx.core.strategy.optimizer import strategy_optimizer

class EvolutionTracker:
    """Logs the macroscopic shifts in system intelligence."""
    
    def __init__(self):
        self.history = []
        
    def log_cycle(self, cycle_number: int):
        snapshot = dict(strategy_optimizer.capability_weights)
        self.history.append({
            "cycle": cycle_number,
            "timestamp": time.time(),
            "weights": snapshot
        })
        
    def print_evolution_report(self):
        print(f"\n[EVOLUTION TRACKER] Intelligence Drift History:")
        for h in self.history:
            print(f"  Cycle {h['cycle']}: {h['weights']}")

evolution_tracker = EvolutionTracker()
