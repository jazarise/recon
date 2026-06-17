import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command("start")
def start_scan(target: str):
    console.print(f"[green]Starting scan on[/green] {target}")
    # connect to core/orchestrator logic here
