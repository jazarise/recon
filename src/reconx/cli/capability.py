import typer
from rich.console import Console
from rich.table import Table
from reconx.core.registry import capability_registry, load_adapters

app = typer.Typer()
console = Console()

@app.command("list")
def list_capabilities():
    """List all registered capabilities."""
    load_adapters()  # Ensure adapters are registered
    table = Table(title="ReconX Capabilities")
    table.add_column("Capability Name", style="cyan", no_wrap=True)
    table.add_column("Category", style="magenta")
    table.add_column("Adapters", style="green")
    table.add_column("Description")

    capabilities = capability_registry.list_capabilities()
    for cap in capabilities:
        adapters = ", ".join(cap.adapters) if cap.adapters else "None"
        table.add_row(cap.name, cap.category.value, adapters, cap.description)
    
    console.print(table)
