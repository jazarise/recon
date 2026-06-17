import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command("generate")
def generate(scan_id: str):
    console.print(f"Generating report for {scan_id}")
