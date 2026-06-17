from typing import Dict, Any


class TrendAnalyzer:
    @staticmethod
    def compare_scans(
        current: Dict[str, Any], previous: Dict[str, Any]
    ) -> Dict[str, Any]:
        cur_assets = len(current.get("assets", []))
        prev_assets = len(previous.get("assets", []))

        cur_findings = len(current.get("findings", []))
        prev_findings = len(previous.get("findings", []))

        cur_risk = current.get("risk_score", 0)
        prev_risk = previous.get("risk_score", 0)

        risk_change = 0
        if prev_risk > 0:
            risk_change = ((cur_risk - prev_risk) / prev_risk) * 100

        return {
            "new_assets": max(0, cur_assets - prev_assets),
            "removed_assets": max(0, prev_assets - cur_assets),
            "new_findings": max(0, cur_findings - prev_findings),
            "resolved_findings": max(0, prev_findings - cur_findings),
            "risk_change_percent": risk_change,
        }
