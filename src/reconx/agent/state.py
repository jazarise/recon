class AgentState:
    def __init__(self):
        self.coverage_percent = 0.0
        self.unique_assets = 0
        self.noise_level = "Low"
        self.confidence = "High"
        self.cycles_without_findings = 0
        self.max_cycles = 20

    def update_findings(self, new_assets: int):
        if new_assets == 0:
            self.cycles_without_findings += 1
        else:
            self.unique_assets += new_assets
            self.cycles_without_findings = 0
            self.coverage_percent = min(100.0, self.coverage_percent + 15.0)

    def should_stop(self) -> bool:
        if self.cycles_without_findings >= 3:
            return True
        return False
