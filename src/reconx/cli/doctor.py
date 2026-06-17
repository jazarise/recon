import typer
from rich.console import Console
from rich.table import Table
from reconx.core.capabilities import capability_manager
from reconx.core.registry import load_adapters

app = typer.Typer()
console = Console()


@app.command("check")
def check():
    """Run health checks on all registered adapters."""
    load_adapters()
    console.print("[blue]Running system health checks...[/blue]")
    health_report = capability_manager.health_check()

    table = Table(title="Adapter Health Status")
    table.add_column("Adapter", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Version", style="magenta")

    for adapter_name, health in health_report.items():
        status = (
            "[green]Installed[/green]"
            if health.get("installed")
            else "[red]Missing[/red]"
        )
        version = health.get("version", "unknown")
        table.add_row(adapter_name, status, version)

    console.print(table)
