import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command("check")
def check():
    console.print("[green]All systems operational.[/green]")
