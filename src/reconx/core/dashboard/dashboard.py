from reconx.core.database.db import DatabaseManager


class DashboardManager:
    def __init__(self, workspace="default"):
        self.db = DatabaseManager(workspace)

    def render_overview(self):
        assets = self.db.query_assets()
        findings = self.db.query_findings()
        critical_findings = [f for f in findings if f.get("severity") == "Critical"]

        return {
            "Total Assets": len(assets),
            "Total Findings": len(findings),
            "Critical Findings": len(critical_findings),
        }
