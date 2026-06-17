import typer
import asyncio
from rich.console import Console
from rich.table import Table
from reconx.core.plugins.manager import plugin_manager
from reconx.core.database.session import async_session_factory
import json

app = typer.Typer(help="Manage and execute plugins")
console = Console()


@app.command("list")
def list_plugins():
    """List all available plugins"""
    plugin_manager.load_all()
    plugins = plugin_manager.list_plugins()

    table = Table(title="Available Plugins")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="magenta")
    table.add_column("Category", style="green")

    for p in plugins:
        table.add_row(p.get("name"), p.get("version"), p.get("category"))

    console.print(table)


@app.command("info")
def info(name: str):
    """Get details about a specific plugin"""
    plugin_manager.load_all()
    plugins = plugin_manager.list_plugins()

    for p in plugins:
        if p.get("name") == name:
            console.print(json.dumps(p, indent=2))
            return

    console.print(f"[red]Plugin {name} not found[/red]")


@app.command("run")
def run_plugin(name: str, target: str):
    """Execute a plugin against a target"""

    async def _run():
        console.print(f"[blue]Running {name} against {target}...[/blue]")
        async with async_session_factory() as db:
            result = await plugin_manager.execute_plugin(db, name, "cli_target", target)
            console.print(f"[green]Status: {result.status}[/green]")
            if result.findings:
                console.print(f"Found {len(result.findings)} findings.")
            if result.errors:
                for err in result.errors:
                    console.print(f"[red]Error: {err}[/red]")

    asyncio.run(_run())


@app.command("reload")
def reload():
    """Reload all plugins"""
    plugin_manager.load_all()
    console.print("[green]Plugins reloaded successfully.[/green]")
