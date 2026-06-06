import typer
import asyncio
from rich.console import Console
from rich.table import Table
from reconx.config.settings import settings
from reconx.plugins.loader import PluginManager

app = typer.Typer(
    name="reconx",
    help="ReconX: Unified Cyber Intelligence OS",
    no_args_is_help=True,
    add_completion=False
)
console = Console()

@app.command()
def init():
    """Initialize ReconX database and configurations."""
    console.print("[green]Initializing ReconX...[/green]")
    # TODO: Run alembic migrations or create_all()
    console.print("[green]Initialization complete.[/green]")

@app.command()
def doctor():
    """Check system environment and plugin dependencies."""
    console.print("[bold blue]Running ReconX environment checks...[/bold blue]")
    
    loader = PluginManager()
    plugins = loader.load_plugins()
    
    table = Table("Plugin", "Version", "Capabilities", "Status")
    for name, plugin_cls in plugins.items():
        plugin = plugin_cls()
        is_valid = asyncio.run(plugin.validate())
        status = "[green]OK[/green]" if is_valid else "[red]Missing dependencies[/red]"
        table.add_row(name, plugin.version, ", ".join(plugin.capabilities), status)
        
    console.print(table)
    console.print("[green]Environment checks complete.[/green]")

@app.command()
def run(target: str, plugin: str = typer.Option(..., help="Plugin to execute")):
    """Run a specific plugin against a target."""
    console.print(f"Running scan against [bold]{target}[/bold] using plugin [bold]{plugin}[/bold]...")
    loader = PluginManager()
    plugins = loader.load_plugins()
    
    if plugin not in plugins:
        console.print(f"[red]Error: Plugin '{plugin}' not found.[/red]")
        raise typer.Exit(code=1)
        
    plugin_instance = plugins[plugin]()
    
    async def _run():
        if not await plugin_instance.validate():
             console.print(f"[red]Error: Plugin '{plugin}' dependencies are missing.[/red]")
             return
        findings = await plugin_instance.execute(target=target)
        console.print(f"[green]Scan complete! Found {len(findings)} findings.[/green]")
        for f in findings:
            console.print(f" - {f.finding_type}: {f.raw_output}")
            
    asyncio.run(_run())

@app.command()
def findings():
    """List recent findings."""
    console.print("[blue]Recent findings (Mock UI)[/blue]")
    # TODO: fetch from DB
    console.print("No findings yet.")

@app.command()
def plugins():
    """List available plugins."""
    loader = PluginManager()
    plugins = loader.load_plugins()
    
    table = Table("Plugin", "Version", "Capabilities")
    for name, plugin_cls in plugins.items():
         table.add_row(name, plugin_cls.version, ", ".join(plugin_cls.capabilities))
    console.print(table)

@app.command()
def config():
    """Show current configuration."""
    console.print("[blue]Current ReconX Configuration:[/blue]")
    console.print(settings.model_dump())
    
@app.command()
def dashboard(dev: bool = typer.Option(False, "--dev", help="Run in development mode")):
    """Start the ReconX dashboard."""
    if dev:
        console.print("[yellow]Starting dashboard in DEV mode (backend only).[/yellow]")
        console.print("Run 'npm run dev' in reconx/dashboard/frontend for the UI.")
    else:
        console.print("[green]Starting production dashboard...[/green]")
        console.print("Assuming frontend is built in reconx/dashboard/frontend/dist")
    
    # uvicorn.run("reconx.dashboard.api:app", host=settings.API_HOST, port=settings.API_PORT, reload=dev)
    console.print(f"Server would start at {settings.API_HOST}:{settings.API_PORT}")

if __name__ == "__main__":
    app()
