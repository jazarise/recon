import typer
from rich.console import Console
from core.workflow_engine import workflow_engine
import asyncio
from core.orchestrator import orchestrator

app = typer.Typer()
console = Console()

@app.command("run")
def run_workflow(name: str, target: str):
    console.print(f"[blue]Running workflow[/blue] {name} [blue]on[/blue] {target}")
    asyncio.run(orchestrator.run_workflow(name, target))
    console.print(f"[bold green]Workflow {name} completed![/bold green]")
