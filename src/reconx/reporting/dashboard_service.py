from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from reconx.core.database.models import Asset, Finding
from reconx.core.intelligence.risk_scoring import RiskScoring
from reconx.reporting.trend_analyzer import TrendAnalyzer


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_metrics(self) -> Dict[str, Any]:
        assets_res = await self.db.execute(select(Asset))
        assets = assets_res.scalars().all()

        findings_res = await self.db.execute(select(Finding))
        findings = findings_res.scalars().all()

        f_dicts = [
            {
                "severity": f.severity.name,
                "asset_value": getattr(f, "asset_value", "Unknown"),
            }
            for f in findings
        ]
        risk_score = RiskScoring.calculate_project_score(f_dicts)

        critical_count = len([f for f in f_dicts if f["severity"] == "CRITICAL"])
        high_count = len([f for f in f_dicts if f["severity"] == "HIGH"])
        medium_count = len([f for f in f_dicts if f["severity"] == "MEDIUM"])
        low_count = len([f for f in f_dicts if f["severity"] == "LOW"])
        info_count = len([f for f in f_dicts if f["severity"] == "INFO"])

        # Fake trend for demonstration
        trend = TrendAnalyzer.compare_scans(
            {"assets": assets, "findings": findings, "risk_score": risk_score},
            {"assets": [], "findings": [], "risk_score": 0},
        )

        return {
            "total_assets": len(assets),
            "risk_score": risk_score,
            "critical_findings": critical_count,
            "high_findings": high_count,
            "medium_findings": medium_count,
            "low_findings": low_count,
            "info_findings": info_count,
            "trends": trend,
        }
