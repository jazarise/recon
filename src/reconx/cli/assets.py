import typer
import asyncio
from rich.console import Console
from reconx.core.database.session import async_session_factory
from reconx.core.intelligence.intelligence_store import IntelligenceStore
from reconx.core.intelligence.risk_scoring import RiskScoring
from sqlalchemy import select
from reconx.core.database.models import Finding

app = typer.Typer(help="Manage Intelligence Data")
console = Console()


@app.command("list")
def list_assets():
    """List all assets"""

    async def _run():
        async with async_session_factory() as db:
            store = IntelligenceStore(db)
            assets = await store.get_assets()
            for a in assets:
                console.print(f"[{a['type']}] {a['value']} (Source: {a['source']})")

    asyncio.run(_run())


@app.command("show")
def show_asset(id: str):
    """Show asset graph"""

    async def _run():
        async with async_session_factory() as db:
            store = IntelligenceStore(db)
            graph = await store.get_asset_graph()
            console.print(graph)

    asyncio.run(_run())


@app.command("findings")
def list_findings():
    """List all findings"""

    async def _run():
        async with async_session_factory() as db:
            res = await db.execute(select(Finding))
            for f in res.scalars().all():
                console.print(f"[{f.severity.name}] {f.title}")

    asyncio.run(_run())


@app.command("risk")
def risk_summary():
    """Show risk summary"""

    async def _run():
        async with async_session_factory() as db:
            res = await db.execute(select(Finding))
            findings = [{"severity": f.severity.name} for f in res.scalars().all()]
            score = RiskScoring.calculate_project_score(findings)
            console.print(
                f"Project Risk Score: {score} (Total Findings: {len(findings)})"
            )

    asyncio.run(_run())
