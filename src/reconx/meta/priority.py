class AutonomousScheduler:
    @staticmethod
    def determine_frequency(risk_score: float) -> str:
        if risk_score >= 0.8:
            return "Continuous (1h polling)"
        elif risk_score >= 0.5:
            return "Periodic (24h polling)"
        return "Archived (7d polling)"
