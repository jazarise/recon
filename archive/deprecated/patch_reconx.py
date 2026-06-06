import os
import sys
from pathlib import Path

BASE_DIR = Path("e:/ReconX/Reconx_V_2.0.0")

def patch_reconx():
    reconx_path = BASE_DIR / "reconx.py"
    with open(reconx_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    patch = """
def cmd_plugins():
    from core.plugin_manager.loader import PluginManager
    pm = PluginManager()
    pm.discover_and_load()
    print("Loaded Plugins:")
    for name, plugin in pm.plugins.items():
        print(f" - {name} (v{plugin.version})")

def cmd_run(plugin_name: str, target: str):
    from core.plugin_manager.loader import PluginManager
    pm = PluginManager()
    pm.discover_and_load()
    if plugin_name not in pm.plugins:
        print(f"Error: Plugin {plugin_name} not found")
        return
    plugin = pm.plugins[plugin_name]
    print(f"Running {plugin_name} against {target}...")
    results = plugin.run(target=target)
    normalized = plugin.normalize(results)
    for n in normalized:
        print(n.model_dump_json())

def cmd_workflow(workflow_name: str, target: str):
    import asyncio
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    proj = pm.get_project("default_project")
    if not proj:
        pm.create_project("default_project", target, "Default", [])
    
    wf_file = f"{workflow_name}.yaml"
    result = asyncio.run(_run_workflow(wf_file, target, "default_project"))
    _print_workflow_result(result)
"""
    if "def cmd_plugins()" not in content:
        # insert before def main():
        content = content.replace("def main():", patch + "\ndef main():")
        
        # update help text
        content = content.replace(
            "update           Check tool availability",
            "update           Check tool availability\n  plugins          List loaded plugins\n  run              Run a specific plugin\n  workflow         Run a specific workflow"
        )
        
        # update choices
        content = content.replace(
            'choices=["scan", "dashboard", "doctor", "projects",\n                 "status", "report", "recipes", "update"]',
            'choices=["scan", "dashboard", "doctor", "projects",\n                 "status", "report", "recipes", "update", "plugins", "run", "workflow"]'
        )
        
        # update arg parsing logic
        arg_logic = """
    elif args.command == "plugins":
        cmd_plugins()
    elif args.command == "run":
        if len(args.args) < 1 or not args.target:
            print("Usage: reconx run <plugin> -t <target>")
            sys.exit(1)
        cmd_run(args.args[0], args.target)
    elif args.command == "workflow":
        if len(args.args) < 1 or not args.target:
            print("Usage: reconx workflow <workflow> -t <target>")
            sys.exit(1)
        cmd_workflow(args.args[0], args.target)
"""
        content = content.replace(
            '    else:\n        # Full interactive mode\n        interactive_menu()',
            arg_logic + '    else:\n        # Full interactive mode\n        interactive_menu()'
        )

    with open(reconx_path, "w", encoding="utf-8") as f:
        f.write(content)
        
if __name__ == "__main__":
    patch_reconx()
