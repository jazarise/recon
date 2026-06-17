import typer
import asyncio
from rich.console import Console
from reconx.core.database.session import async_session_factory
from reconx.reporting.report_engine import ReportEngine
from reconx.reporting.dashboard_service import DashboardService

app = typer.Typer(help="Manage Reporting and Dashboards")
console = Console()


@app.command("generate")
def generate(format: str = "json"):
    """Generate a report in the specified format"""

    async def _run():
        async with async_session_factory() as db:
            engine = ReportEngine(db)
            path = await engine.export_report(format)
            console.print(f"Report generated successfully: {path}")

    asyncio.run(_run())


@app.command("export")
def export(format: str = "csv"):
    """Export data"""
    generate(format)


@app.command("dashboard")
def dashboard():
    """View dashboard summary"""

    async def _run():
        async with async_session_factory() as db:
            service = DashboardService(db)
            metrics = await service.get_metrics()
            console.print(metrics)

    asyncio.run(_run())
