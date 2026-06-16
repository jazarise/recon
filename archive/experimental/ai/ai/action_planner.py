class ActionPlanner:
    def plan(self, context: dict, risk_score: int) -> list:
        """Generates subsequent recon actions based on risk and context."""
        asset = context.get("asset", {})
        actions = []
        
        asset_type = asset.get("type", "").upper()
        
        if risk_score >= 70:
            actions.append(f"Trigger full vulnerability scan (nuclei) on {asset.get('value')}")
            
        if asset_type == "SUBDOMAIN":
            actions.append(f"Perform deep port scan on underlying IPs for {asset.get('value')}")
            
        if asset_type == "IP":
            actions.append(f"Run detailed service enumeration on {asset.get('value')}")
            
        if not actions:
            actions.append(f"Continue passive monitoring of {asset.get('value')}")
            
        return actions

action_planner = ActionPlanner()
