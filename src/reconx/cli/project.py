import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command("list")
def list_projects():
    console.print("Listing projects...")
