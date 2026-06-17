from typing import List, Dict, Any


class RiskScoring:
    SEVERITY_WEIGHTS = {"CRITICAL": 10, "HIGH": 7, "MEDIUM": 5, "LOW": 3, "INFO": 1}

    @staticmethod
    def calculate_project_score(findings: List[Dict[str, Any]]) -> int:
        score = 0
        for f in findings:
            sev = str(f.get("severity", "INFO")).upper()
            score += RiskScoring.SEVERITY_WEIGHTS.get(sev, 0)
        return score

    @staticmethod
    def calculate_asset_score(
        asset_findings: List[Dict[str, Any]], exposure: int = 0, sensitivity: int = 0
    ) -> int:
        finding_score = sum(
            RiskScoring.SEVERITY_WEIGHTS.get(str(f.get("severity", "INFO")).upper(), 0)
            for f in asset_findings
        )
        return finding_score + exposure + sensitivity
