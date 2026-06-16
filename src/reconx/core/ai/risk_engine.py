class RiskEngine:
    def calculate_risk(self, context: dict) -> int:
        """Calculates a dynamic risk score between 0 and 100."""
        score = 10
        asset = context.get("asset", {})
        finding = context.get("finding", {})
        
        # Heuristic 1: Asset Type
        asset_type = asset.get("type", "").upper()
        if asset_type in ["IP", "SUBDOMAIN"]:
            score += 20
        elif asset_type == "EMAIL":
            score += 5
            
        # Heuristic 2: Findings
        if finding:
            severity = finding.get("severity", "").upper()
            if severity == "CRITICAL":
                score += 60
            elif severity == "HIGH":
                score += 40
            elif severity == "MEDIUM":
                score += 20
                
        # Heuristic 3: Keywords
        value = asset.get("value", "").lower()
        if any(keyword in value for keyword in ["admin", "api", "dev", "test", "internal"]):
            score += 15
            
        return min(score, 100)

risk_engine = RiskEngine()
