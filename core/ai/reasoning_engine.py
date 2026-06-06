class ReasoningEngine:
    def evaluate(self, context: dict, risk_score: int) -> str:
        """Simulates AI natural language reasoning."""
        asset = context.get("asset", {})
        finding = context.get("finding", {})
        
        reasons = []
        if risk_score >= 90:
            reasons.append("This is a CRITICAL risk asset.")
        elif risk_score >= 70:
            reasons.append("This is a HIGH risk asset.")
            
        value = asset.get("value", "").lower()
        if "admin" in value:
            reasons.append("It appears to be an administrative interface, which greatly increases exposure impact.")
        if "api" in value:
            reasons.append("It exposes an API, expanding the programmatic attack surface.")
            
        if finding:
            reasons.append(f"It is actively affected by a {finding.get('severity', 'UNKNOWN')} severity finding.")
            
        if not reasons:
            return "This asset has standard exposure with no immediate critical indicators."
            
        return " ".join(reasons)

    def generate_attack_path(self, context: dict) -> list:
        """Simulates building a graph path for exploitation."""
        asset = context.get("asset", {})
        finding = context.get("finding", {})
        
        path = ["Internet", asset.get("value", "Asset")]
        if finding:
            path.append(finding.get("title", "Vulnerability"))
            path.append("Exploitation")
            
        return path

reasoning_engine = ReasoningEngine()
