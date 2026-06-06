class RiskEngine:
    SEVERITY_SCORES = {
        "critical": 95,
        "high": 80,
        "medium": 55,
        "low": 20,
        "info": 5
    }

    def calculate_finding_score(self, severity: str) -> int:
        return self.SEVERITY_SCORES.get(severity.lower(), 0)

    def calculate_asset_risk(self, findings: list) -> int:
        if not findings:
            return 0
            
        scores = [self.calculate_finding_score(getattr(f, 'severity', 'info')) for f in findings]
        base_score = max(scores)
        additional_weight = sum(s * 0.1 for s in scores)
        
        final_score = min(100, int(base_score + additional_weight))
        return final_score

risk_engine = RiskEngine()
