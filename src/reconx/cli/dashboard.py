import typer
import subprocess  # nosec B404
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command("start")
def start():
    console.print("[green]Starting dashboard on http://127.0.0.1:8000[/green]")
    subprocess.run(["uvicorn", "api.main:app", "--reload"])  # nosec B603 B607, "api.main:app", "--reload"])
