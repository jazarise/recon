from typing import Dict, Any, List


class ExecutiveSummaryGenerator:
    @staticmethod
    def generate(
        assets: List[Dict[str, Any]], findings: List[Dict[str, Any]], risk_score: int
    ) -> Dict[str, Any]:
        high_risk_findings = [
            f for f in findings if f.get("severity") in ["HIGH", "CRITICAL"]
        ]

        # very basic calculation for "most exposed"
        asset_counts: Dict[str, int] = {}
        for f in findings:
            a_val = str(f.get("asset_value", "Unknown"))
            asset_counts[a_val] = asset_counts.get(a_val, 0) + 1

        most_exposed = (
            max(asset_counts, key=lambda k: asset_counts[k]) if asset_counts else "None"
        )

        return {
            "total_assets": len(assets),
            "high_risk_findings": len(high_risk_findings),
            "most_exposed_asset": most_exposed,
            "project_risk_score": risk_score,
            "recommendations": [
                "Prioritize remediation of internet-facing APIs.",
                "Review critical vulnerabilities immediately.",
            ],
        }
