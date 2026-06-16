from core.asm.scheduler import asm_scheduler

class AsmEngine:
    """The central orchestrator for the Continuous ASM system."""
    
    def __init__(self):
        self.scheduler = asm_scheduler

    def start_monitoring(self, target: str, capabilities: list, interval_seconds: int = 3600):
        """Starts a continuous monitoring job for a target."""
        from core.capabilities import capability_manager
        
        def run_scan():
            print(f"[*] ASM Engine executing scheduled scan on {target}...")
            for cap in capabilities:
                capability_manager.run(cap, target)

        job_name = f"monitor_{target}"
        self.scheduler.schedule_job(job_name, interval_seconds, run_scan)

asm_engine = AsmEngine()
