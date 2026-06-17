import typer
import asyncio
from rich.console import Console
from reconx.core.workflow.workflow_engine import workflow_engine
from reconx.core.workflow.state_manager import StateManager
from reconx.core.database.session import async_session_factory
import glob
import os

app = typer.Typer(help="Manage workflows")
console = Console()


@app.command("list")
def list_workflows():
    """List all available workflows"""
    console.print("Available workflows:")
    for f in glob.glob("src/reconx/workflows/*.yaml"):
        console.print(f"- {os.path.basename(f).replace('.yaml', '')}")


@app.command("run")
def run_workflow(name: str, target: str):
    """Execute a workflow against a target"""

    async def _run():
        console.print(f"[blue]Running workflow {name} against {target}...[/blue]")
        result = await workflow_engine.execute_workflow(name, target)
        if result["status"] == "SUCCESS":
            console.print("[green]Workflow completed successfully.[/green]")
        else:
            console.print("[red]Workflow failed.[/red]")
        console.print(f"Execution ID: {result['execution_id']}")

    asyncio.run(_run())


@app.command("status")
def status(id: str):
    """Check workflow status"""

    async def _status():
        async with async_session_factory() as db:
            state_manager = StateManager(db)
            record = await state_manager.get_execution(id)
            if not record:
                console.print("[red]Execution not found[/red]")
                return
            console.print(f"Status: {record.status}")
            console.print(f"Started: {record.started_at}")
            if record.finished_at:
                console.print(f"Finished: {record.finished_at}")

    asyncio.run(_status())


@app.command("cancel")
def cancel(id: str):
    """Cancel a running workflow"""

    async def _cancel():
        async with async_session_factory() as db:
            state_manager = StateManager(db)
            record = await state_manager.get_execution(id)
            if not record:
                console.print("[red]Execution not found[/red]")
                return
            await state_manager.update_status(id, "CANCELLED")
            console.print("[green]Workflow cancelled.[/green]")

    asyncio.run(_cancel())
