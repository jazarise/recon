#!/usr/bin/env python3
"""
ReconX — Unified Reconnaissance Orchestration Platform
Interactive CLI, project management, and workflow runner.
"""

import sys
import os
import asyncio
import argparse
from pathlib import Path

# Ensure project root is in path before any local imports
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.config import config
from core.paths import WORKFLOWS_DIR

__version__ = "1.0.0"

# ── Rich TUI setup ────────────────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.progress import (
        Progress, SpinnerColumn, BarColumn,
        TaskProgressColumn, TextColumn, TimeElapsedColumn,
    )
    from rich.columns import Columns
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

console = Console() if HAS_RICH else None


# ─── Banner ───────────────────────────────────────────────────────────────────

def print_banner():
    if not HAS_RICH:
        print(f"\n{'='*54}\nRECONX v{__version__}\nUnified Reconnaissance Platform\n{'='*54}\n")
        return
    banner = Text()
    banner.append("\n")
    banner.append("██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗\n", style="bold red")
    banner.append("██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝\n", style="bold red")
    banner.append("██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ \n", style="bold bright_red")
    banner.append("██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ \n", style="bold bright_red")
    banner.append("██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗\n", style="red")
    banner.append("╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝\n", style="red")
    console.print(banner, justify="center")
    console.print(
        f"[dim]Unified Reconnaissance Platform  ·  v{__version__}  ·  "
        "[bold red]Authorized use only[/bold red][/dim]\n",
        justify="center",
    )


# ─── Scan-profile catalogue ───────────────────────────────────────────────────

SCAN_PROFILES = {
    "1": ("Basic",          "basic.yaml",     "Fast discovery — ~5-15 min"),
    "2": ("Medium",         "medium.yaml",    "Balanced scan — ~15-60 min"),
    "3": ("Deep",           "deep.yaml",      "Maximum intel — ~1-6+ hrs"),
}

SCAN_PROFILE_MENU = """
 [bold white]Choose Scan Type[/bold white]

  [bold cyan]1.[/bold cyan]  Basic           [dim]Fast discovery, passive DNS, HTTP probe[/dim]
  [bold cyan]2.[/bold cyan]  Medium          [dim]Adds port scan + LLM analysis[/dim]
  [bold cyan]3.[/bold cyan]  Deep            [dim]Full-depth intel gathering[/dim]
"""

# ─── Utilities ────────────────────────────────────────────────────────────────

def _print(msg, style=""):
    if HAS_RICH:
        console.print(msg, style=style)
    else:
        print(msg)


def _ask(prompt, default=""):
    if HAS_RICH:
        return Prompt.ask(prompt, default=default)
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default


def _confirm(prompt, default=True):
    if HAS_RICH:
        return Confirm.ask(prompt, default=default)
    val = input(f"{prompt} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
    if not val:
        return default
    return val.startswith("y")


def _separator():
    if HAS_RICH:
        console.rule(style="dim red")


# ─── Core run scan helper ─────────────────────────────────────────────────────

async def _run_workflow(workflow_file: str, target: str, project: str):
    from events.event_bus import EventBus
    from core.workflow_engine import WorkflowEngine
    from core.plugin_loader import PluginLoader
    from core.execution_manager import ExecutionManager
    from core.orchestrator import Orchestrator
    from core.result_store import ResultStore
    from core.project_manager import ProjectManager

    event_bus = EventBus()
    plugin_loader = PluginLoader()
    plugin_loader.discover_and_load()
    execution_manager = ExecutionManager(event_bus=event_bus, plugin_loader=plugin_loader)
    workflow_engine = WorkflowEngine(execution_manager=execution_manager, event_bus=event_bus)
    result_store = ResultStore(project_name=project)

    orchestrator = Orchestrator(
        event_bus=event_bus,
        workflow_engine=workflow_engine,
        execution_manager=execution_manager,
        result_store=result_store,
    )

    # Live TUI event hooks
    step_statuses: dict = {}

    def on_plugin_started(p):
        name = p.get("plugin", "?")
        step_statuses[name] = "RUNNING"
        if HAS_RICH:
            console.print(f"  [yellow]▶[/yellow] [bold]{name}[/bold]  [dim]starting…[/dim]")

    def on_plugin_completed(p):
        name = p.get("plugin", "?")
        step_statuses[name] = "SUCCESS"
        if HAS_RICH:
            console.print(f"  [green]✓[/green] [bold]{name}[/bold]  [dim]completed[/dim]")

    def on_plugin_failed(p):
        name = p.get("plugin", "?")
        err = p.get("error", "unknown error")
        step_statuses[name] = "FAILED"
        if HAS_RICH:
            console.print(f"  [red]✗[/red] [bold]{name}[/bold]  [dim]{err}[/dim]")

    event_bus.subscribe("plugin_started", on_plugin_started)
    event_bus.subscribe("plugin_completed", on_plugin_completed)
    event_bus.subscribe("plugin_failed", on_plugin_failed)

    await orchestrator.start()

    wf_path = Path(workflow_file)
    if not wf_path.exists():
        wf_path = WORKFLOWS_DIR / workflow_file
    if not wf_path.exists():
        _print(f"[red]✗ Workflow not found: {workflow_file}[/red]")
        return None

    _separator()
    if HAS_RICH:
        console.print(Panel.fit(
            f"[bold white]Target:[/bold white]  [cyan]{target}[/cyan]\n"
            f"[bold white]Profile:[/bold white] [cyan]{wf_path.stem}[/cyan]\n"
            f"[bold white]Project:[/bold white] [cyan]{project}[/cyan]",
            title="[bold red]ReconX Live Execution[/bold red]",
            border_style="red",
        ))
    else:
        print(f"\nTarget: {target}  |  Profile: {wf_path.stem}  |  Project: {project}\n")

    result = await orchestrator.run_workflow(str(wf_path), target, project_name=project)

    # Update project metadata
    try:
        pm = ProjectManager()
        pm.update_project_scan(project)
    except Exception:
        pass

    return result


def _print_workflow_result(result: dict):
    if not result:
        return
    _separator()
    steps = result.get("steps", [])
    passed = sum(1 for s in steps if s.get("status") == "completed")
    failed = sum(1 for s in steps if s.get("status") == "failed")

    if HAS_RICH:
        console.print(f"\n[bold green]✓ Workflow Complete[/bold green]  "
                      f"[green]{passed} passed[/green]  [red]{failed} failed[/red]\n")

        # Show output file paths from reporting step
        for step in steps:
            if step.get("plugin") == "reporting":
                out = step.get("output", {})
                reports = out.get("reports", {})
                if reports:
                    console.print("[bold white]Reports generated:[/bold white]")
                    for fmt, path in reports.items():
                        console.print(f"  [cyan]{fmt.upper():<8}[/cyan] {path}")
    else:
        print(f"\nWorkflow Complete — {passed} passed, {failed} failed")


# ─── Sub-commands ─────────────────────────────────────────────────────────────

def cmd_doctor():
    """Run full system health check."""
    from core.doctor import Doctor
    _print("\n[bold red]ReconX Doctor[/bold red] — System Health Check\n")
    doc = Doctor()
    checks = doc.run_all()

    if HAS_RICH:
        t = Table(box=box.ROUNDED, border_style="dim", show_header=True, header_style="bold")
        t.add_column("Check", style="white", min_width=30)
        t.add_column("Status", justify="center", min_width=8)
        t.add_column("Detail", style="dim")
        t.add_column("Fix", style="yellow dim")

        for c in checks:
            s = c["status"]
            if s is True:
                badge = "[bold green]PASS[/bold green]"
            elif s is False:
                badge = "[bold red]FAIL[/bold red]"
            else:
                badge = "[bold yellow]WARN[/bold yellow]"
            t.add_row(c["name"], badge, c["detail"] or "", c["fix"] or "")

        console.print(t)
        summ = doc.summary()
        console.print(
            f"\n[green]{summ['passed']} passed[/green]  "
            f"[red]{summ['failed']} failed[/red]  "
            f"[yellow]{summ['warned']} warnings[/yellow]\n"
        )
    else:
        for c in checks:
            s = "PASS" if c["status"] is True else ("FAIL" if c["status"] is False else "WARN")
            print(f"[{s}] {c['name']}: {c['detail']}")


def cmd_projects():
    """List all projects."""
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    projects = pm.list_projects()

    if not projects:
        _print("\n[dim]No projects found. Run [bold]reconx[/bold] to create one.[/dim]\n")
        return

    _print(f"\n[bold]Projects ({len(projects)})[/bold]\n")
    if HAS_RICH:
        t = Table(box=box.ROUNDED, border_style="dim")
        t.add_column("Name", style="cyan")
        t.add_column("Target", style="white")
        t.add_column("Status", style="green")
        t.add_column("Scans", justify="right")
        t.add_column("Last Scan", style="dim")
        for p in projects:
            t.add_row(
                p["name"],
                p.get("target", "—"),
                p.get("status", "new"),
                str(p.get("scan_count", 0)),
                (p.get("last_scan") or "never")[:19],
            )
        console.print(t)
    else:
        for p in projects:
            print(f"  {p['name']:<20} {p.get('target',''):<30} scans={p.get('scan_count',0)}")


def cmd_status():
    """Show active/recent jobs."""
    from core.paths import PROJECT_ROOT
    import json
    outputs_dir = PROJECT_ROOT / "outputs"
    files = sorted(outputs_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)[:10]

    if not files:
        _print("\n[dim]No recent job results found.[/dim]\n")
        return

    _print(f"\n[bold]Recent Jobs[/bold]\n")
    if HAS_RICH:
        t = Table(box=box.ROUNDED, border_style="dim")
        t.add_column("Workflow ID", style="dim", max_width=20)
        t.add_column("Target", style="cyan")
        t.add_column("Status", style="green")
        t.add_column("Started", style="dim")
        for f in files:
            try:
                with open(f) as fh:
                    d = json.load(fh)
                t.add_row(
                    d.get("workflow_id", "?")[:18],
                    d.get("target", "?"),
                    d.get("status", "?"),
                    (d.get("started_at") or "?")[:19],
                )
            except Exception:
                pass
        console.print(t)
    else:
        for f in files:
            print(f"  {f.stem}")


def cmd_scan(project_name: str, profile: str, target: str = None):
    """Run a scan on an existing project."""
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    proj = pm.get_project(project_name)

    if not proj:
        _print(f"[red]Project '{project_name}' not found. Use [bold]reconx[/bold] to create it.[/red]")
        return

    scan_target = target or proj.get("target", "")
    if not scan_target:
        scan_target = _ask("Target")

    _, wf_file, _ = SCAN_PROFILES.get(profile, SCAN_PROFILES["1"])
    result = asyncio.run(_run_workflow(wf_file, scan_target, project_name))
    _print_workflow_result(result)


def cmd_report(project_name: str):
    """List generated reports for a project."""
    from core.paths import PROJECT_ROOT
    proj_reports = PROJECT_ROOT / "outputs"
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    proj = pm.get_project(project_name)
    if not proj:
        _print(f"[red]Project '{project_name}' not found.[/red]")
        return

    patterns = list(proj_reports.glob(f"report_*"))
    if not patterns:
        _print(f"\n[dim]No reports found for project '{project_name}'.[/dim]\n")
        return

    _print(f"\n[bold]Reports for {project_name}[/bold]\n")
    for p in sorted(patterns, key=lambda f: f.stat().st_mtime, reverse=True):
        _print(f"  [cyan]{p.name}[/cyan]")
    _print("")


def cmd_dashboard():
    """Launch the ReconX API gateway + dashboard."""
    try:
        import uvicorn
        host = config.get("dashboard.host", "127.0.0.1")
        port = int(config.get("dashboard.port", 8000))
        _print(f"\n[bold green]Starting ReconX Dashboard[/bold green]")
        _print(f"  [cyan]http://{host}:{port}[/cyan]\n")
        uvicorn.run("api.gateway.main:app", host=host, port=port, reload=False)
    except ImportError:
        _print("[red]uvicorn not installed. Run: pip install uvicorn[/red]")
    except Exception as e:
        _print(f"[red]Dashboard error: {e}[/red]")


def cmd_update():
    """Check and report on tool availability (read-only update scan)."""
    import shutil
    _print("\n[bold]ReconX Tool Status[/bold]\n")
    from core.doctor import OPTIONAL_TOOLS
    found, missing = [], []
    for tool, desc in OPTIONAL_TOOLS:
        if shutil.which(tool):
            found.append(tool)
        else:
            missing.append((tool, desc))

    if HAS_RICH:
        if found:
            console.print(f"[green]Found ({len(found)}):[/green] " + ", ".join(found))
        if missing:
            console.print(f"\n[yellow]Not found ({len(missing)}) — install for full capability:[/yellow]")
            for t, d in missing:
                console.print(f"  [dim]{t:<15}[/dim] {d}")
    else:
        print(f"Found: {', '.join(found)}")
        print(f"Missing: {', '.join(t for t, _ in missing)}")
    _print("")


# ─── Interactive main menu ────────────────────────────────────────────────────

def interactive_menu():
    """Full interactive TUI per the Master Product Spec."""
    print_banner()

    while True:
        _separator()
        if HAS_RICH:
            console.print("""
 [bold white]Select Option[/bold white]

  [bold cyan]1.[/bold cyan]  Create Project
  [bold cyan]2.[/bold cyan]  Open Existing Project
  [bold cyan]3.[/bold cyan]  Recent Projects
  [bold cyan]4.[/bold cyan]  Dashboard
  [bold cyan]5.[/bold cyan]  Settings
  [bold cyan]6.[/bold cyan]  Doctor
  [bold cyan]7.[/bold cyan]  Exit
""")
        else:
            print("\n1. Create Project\n2. Open Existing Project\n3. Recent Projects"
                  "\n4. Dashboard\n5. Settings\n6. Doctor\n7. Exit\n")

        choice = _ask("[bold red]>[/bold red]", default="1")

        if choice == "1":
            _flow_create_project()
        elif choice == "2":
            _flow_open_project()
        elif choice == "3":
            _flow_recent_projects()
        elif choice == "4":
            cmd_dashboard()
        elif choice == "5":
            _flow_settings()
        elif choice == "6":
            cmd_doctor()
        elif choice == "7":
            _print("\n[dim]Goodbye.[/dim]\n")
            sys.exit(0)
        else:
            _print("[red]Invalid selection.[/red]")


def _flow_create_project():
    """Project creation wizard."""
    _print("\n[bold]Create New Project[/bold]\n")
    name = _ask("  Project Name")
    if not name:
        _print("[red]Project name is required.[/red]")
        return
    target = _ask("  Target (domain / IP / CIDR)")
    if not target:
        _print("[red]Target is required.[/red]")
        return
    description = _ask("  Description", default="")
    tags_raw = _ask("  Tags (comma-separated)", default="")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    from core.project_manager import ProjectManager
    pm = ProjectManager()
    try:
        proj = pm.create_project(name, target, description, tags)
        _print(f"\n[green]✓ Project '{proj['name']}' created.[/green]")
        _print(f"  [dim]Target: {target}[/dim]\n")
        if _confirm("  Launch scan now?", default=True):
            _flow_run_scan(proj["name"], target)
    except FileExistsError:
        _print(f"[yellow]Project '{name}' already exists. Opening it.[/yellow]")
        _flow_run_scan(name, target)
    except Exception as e:
        _print(f"[red]Error creating project: {e}[/red]")


def _flow_open_project():
    """Select and operate on an existing project."""
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    projects = pm.list_projects()

    if not projects:
        _print("\n[dim]No projects found. Create one first.[/dim]\n")
        return

    _print("\n[bold]Select Project[/bold]\n")
    for i, p in enumerate(projects, 1):
        scan_info = f"last scan: {p.get('last_scan','never')[:10]}" if p.get('last_scan') else "never scanned"
        _print(f"  [cyan]{i}.[/cyan]  {p['name']:<20}  [dim]{p.get('target','')}  ({scan_info})[/dim]")

    _print("")
    sel = _ask("Select project number", default="1")
    try:
        idx = int(sel) - 1
        proj = projects[idx]
    except (ValueError, IndexError):
        _print("[red]Invalid selection.[/red]")
        return

    _flow_project_menu(proj)


def _flow_project_menu(proj: dict):
    """Actions menu for an open project."""
    name = proj["name"]
    target = proj.get("target", "")
    _print(f"\n[bold cyan]Project: {name}[/bold cyan]  [dim]→ {target}[/dim]\n")

    if HAS_RICH:
        console.print("""
  [bold cyan]1.[/bold cyan]  Run Scan
  [bold cyan]2.[/bold cyan]  View Reports
  [bold cyan]3.[/bold cyan]  View Assets (DB)
  [bold cyan]4.[/bold cyan]  Back
""")
    else:
        print("  1. Run Scan\n  2. View Reports\n  3. View Assets\n  4. Back\n")

    choice = _ask("[bold red]>[/bold red]", default="1")
    if choice == "1":
        _flow_run_scan(name, target)
    elif choice == "2":
        cmd_report(name)
    elif choice == "3":
        _flow_view_assets(name)
    # 4 → back


def _flow_run_scan(project_name: str, target: str):
    """Scan-type selection and execution."""
    if HAS_RICH:
        console.print(SCAN_PROFILE_MENU)
    else:
        print("\n1. Basic\n2. Medium\n3. Deep\n")

    choice = _ask("[bold red]>[/bold red]", default="1")
    if choice not in SCAN_PROFILES:
        _print("[red]Invalid profile, using Basic.[/red]")
        choice = "1"

    label, wf_file, desc = SCAN_PROFILES[choice]
    _print(f"\n[dim]Selected: {label} — {desc}[/dim]\n")

    result = asyncio.run(_run_workflow(wf_file, target, project_name))
    _print_workflow_result(result)


def _flow_recent_projects():
    """Show the 5 most-recently-scanned projects and let user jump to one."""
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    recent = pm.recent_projects(5)

    if not recent:
        _print("\n[dim]No recent projects.[/dim]\n")
        return

    _print("\n[bold]Recent Projects[/bold]\n")
    for i, p in enumerate(recent, 1):
        last = (p.get("last_scan") or "never")[:10]
        _print(f"  [cyan]{i}.[/cyan]  {p['name']:<20}  [dim]target: {p.get('target','')}  last: {last}[/dim]")

    _print("")
    sel = _ask("Select project (or Enter to go back)", default="")
    if not sel:
        return
    try:
        proj = recent[int(sel) - 1]
        _flow_project_menu(proj)
    except (ValueError, IndexError):
        _print("[red]Invalid selection.[/red]")


def _flow_settings():
    """Display current configuration."""
    from core.paths import PROJECT_ROOT
    _print("\n[bold]Settings[/bold]\n")
    _print(f"  Config file   : [cyan]{PROJECT_ROOT / 'config.yaml'}[/cyan]")
    _print(f"  Dashboard URL : [cyan]http://{config.get('dashboard.host','127.0.0.1')}:{config.get('dashboard.port',8000)}[/cyan]")
    _print(f"  Threads       : [cyan]{config.get('general.threads', 10)}[/cyan]")
    _print(f"  Log level     : [cyan]{config.get('general.log_level','INFO')}[/cyan]")
    _print("\n  [dim]Edit config.yaml to change settings.[/dim]\n")


def _flow_view_assets(project_name: str):
    """Display assets from the project database."""
    from core.database import DatabaseManager
    from core.models import Asset, Service
    db_mgr = DatabaseManager(project_name)
    db = db_mgr.get_session()
    try:
        assets = db.query(Asset).all()
        if not assets:
            _print(f"\n[dim]No assets found for project '{project_name}'.[/dim]\n")
            return

        _print(f"\n[bold]Assets — {project_name}[/bold]\n")
        if HAS_RICH:
            t = Table(box=box.ROUNDED, border_style="dim")
            t.add_column("Type", style="cyan", width=12)
            t.add_column("Value", style="white")
            t.add_column("Tags", style="dim")
            for a in assets:
                t.add_row(a.type, a.value, ", ".join(a.tags or []))
            console.print(t)
        else:
            for a in assets:
                print(f"  [{a.type}] {a.value}")
        _print("")
    finally:
        db.close()


# ─── CLI entry point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="reconx",
        description=f"ReconX v{__version__} — Unified Reconnaissance Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  (no args)        Interactive menu
  scan <project>   Run scan on existing project
  dashboard        Launch web dashboard
  doctor           System health check
  projects         List all projects
  status           Show recent jobs
  report <project> Show report paths for a project
  update           Check tool availability
""",
    )
    parser.add_argument(
        "command", nargs="?",
        choices=["scan", "dashboard", "doctor", "projects",
                 "status", "report", "update"],
        help="Sub-command to run",
    )
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--project", default=None, help="Project name")
    parser.add_argument("--target", default=None, help="Override target")
    parser.add_argument(
        "--profile", default="1",
        choices=["1", "2", "3", "basic", "medium", "deep"],
        help="Scan profile: 1=basic 2=medium 3=deep",
    )
    parser.add_argument("--version", action="version", version=f"ReconX v{__version__}")
    args = parser.parse_args()

    # Normalise profile
    profile_map = {"basic": "1", "medium": "2", "deep": "3"}
    profile = profile_map.get(args.profile, args.profile)

    if args.command == "scan":
        project = args.project or (args.args[0] if args.args else None)
        if not project:
            _print("[red]Usage: reconx scan <project-name> [--target <target>] [--profile 1|2|3][/red]")
            sys.exit(1)
        print_banner()
        cmd_scan(project, profile, args.target)

    elif args.command == "dashboard":
        cmd_dashboard()

    elif args.command == "doctor":
        print_banner()
        cmd_doctor()

    elif args.command == "projects":
        print_banner()
        cmd_projects()

    elif args.command == "status":
        print_banner()
        cmd_status()

    elif args.command == "report":
        project = args.project or (args.args[0] if args.args else None)
        if not project:
            _print("[red]Usage: reconx report <project-name>[/red]")
            sys.exit(1)
        cmd_report(project)

    elif args.command == "update":
        print_banner()
        cmd_update()

    else:
        # Full interactive mode
        interactive_menu()


if __name__ == "__main__":
    main()
