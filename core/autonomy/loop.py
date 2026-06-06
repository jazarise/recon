from core.decision.engine import decision_engine
from core.learning.feedback import learning_engine
from core.evolution.tracker import evolution_tracker

class AutonomyLoop:
    """The central loop: Observe -> Analyze -> Decide -> Execute -> Learn."""
    
    def __init__(self):
        self.cycle_count = 0
        
    def run_cycle(self, target: str, execution_callback):
        self.cycle_count += 1
        print(f"\n[=========================================]")
        print(f"[RECONX STAGE 14] AUTONOMY CYCLE {self.cycle_count}")
        print(f"[=========================================]")
        
        # 1. Decide
        best_capability = decision_engine.decide_next_action(target)
        
        # 2. Execute (Simulated via callback for this test)
        print(f"[*] Executing {best_capability}...")
        results = execution_callback(best_capability, target)
        
        # 3. Learn
        learning_engine.evaluate_scan(
            capability=best_capability,
            target=target,
            new_assets_found=results["assets_found"],
            duration_sec=results["duration"]
        )
        
        # 4. Evolve
        evolution_tracker.log_cycle(self.cycle_count)

autonomy_loop = AutonomyLoop()
