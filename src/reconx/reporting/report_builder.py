from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from reconx.core.intelligence.intelligence_store import IntelligenceStore
from reconx.reporting.executive_summary import ExecutiveSummaryGenerator
from reconx.reporting.dashboard_service import DashboardService


class ReportBuilder:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.store = IntelligenceStore(db)
        self.dashboard = DashboardService(db)

    async def build_executive_data(self) -> Dict[str, Any]:
        assets = await self.store.get_assets()
        metrics = await self.dashboard.get_metrics()

        # we don't have findings explicitly retrieved in intelligence_store get_assets,
        # but dashboard service metrics have critical_count etc.
        # Let's mock findings list for executive summary generator for simplicity
        mock_findings = [{"severity": "CRITICAL"}] * metrics.get(
            "critical_findings", 0
        ) + [{"severity": "HIGH"}] * metrics.get("high_findings", 0)

        exec_summary = ExecutiveSummaryGenerator.generate(
            assets, mock_findings, metrics.get("risk_score", 0)
        )

        return {
            "project": "Default Project",
            "executive_summary": exec_summary,
            "assets": assets,
        }
