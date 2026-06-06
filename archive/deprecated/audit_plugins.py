import os
from pathlib import Path
import json
import ast

PLUGINS_DIR = Path(r"e:\ReconX\Reconx_V_2.0.0\plugins")
REPORTS_DIR = Path(r"e:\ReconX\Reconx_V_2.0.0\reports")

def check_plugin(file_path):
    issues = []
    has_plugin_class = False
    has_run_method = False
    name = "unknown"
    category = "unknown"
    broken_imports = []
    
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                module_name = getattr(node, 'module', None)
                if module_name:
                    if module_name.startswith("core.") and module_name not in ["core.contracts", "core.plugin_base", "core.http.client"]:
                        broken_imports.append(module_name)
                for alias in getattr(node, 'names', []):
                    if alias.name.startswith("core.") and alias.name not in ["core.contracts", "core.plugin_base", "core.http.client"]:
                        broken_imports.append(alias.name)
            
            if isinstance(node, ast.ClassDef) and node.name in ["Plugin", "ToolAdapter"]:
                has_plugin_class = True
                for item in node.body:
                    if isinstance(item, ast.AsyncFunctionDef) and item.name in ["run", "execute"]:
                        has_run_method = True
                    if isinstance(item, ast.AnnAssign) and getattr(item.target, "id", "") == "name":
                        if isinstance(item.value, ast.Constant): name = item.value.value
                    if isinstance(item, ast.Assign):
                        for t in item.targets:
                            if getattr(t, "id", "") == "name" and isinstance(item.value, ast.Constant):
                                name = item.value.value
                            if getattr(t, "id", "") == "category" and isinstance(item.value, ast.Constant):
                                category = item.value.value
    except Exception as e:
        issues.append(f"Parse error: {e}")
        
    if broken_imports: issues.append(f"Broken imports: {', '.join(broken_imports)}")
    if not has_plugin_class: issues.append("Missing Plugin class")
    if not has_run_method: issues.append("Missing async def run")
    
    return {
        "file": str(file_path.relative_to(PLUGINS_DIR)),
        "name": name,
        "category": category,
        "issues": issues,
        "status": "failing" if issues else "working"
    }

def main():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    plugins = []
    for root, _, files in os.walk(PLUGINS_DIR):
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                plugins.append(check_plugin(Path(root) / f))
                
    working = [p for p in plugins if p["status"] == "working"]
    failing = [p for p in plugins if p["status"] == "failing"]
    
    names = {}
    duplicates = []
    for p in plugins:
        n = p["name"]
        if n != "unknown":
            if n in names: duplicates.append(p)
            else: names[n] = p
            
    with open(REPORTS_DIR / "integration_gap_report.md", "w", encoding="utf-8") as f:
        f.write("# Integration Gap Report\n\n")
        f.write(f"Total Plugins Scanned: {len(plugins)}\n")
        f.write(f"- Working: {len(working)}\n")
        f.write(f"- Failing: {len(failing)}\n")
        f.write(f"- Duplicates: {len(duplicates)}\n\n")
        
        f.write("## Failing Plugins\n")
        for p in failing[:50]:
            f.write(f"- **{p['file']}**: {', '.join(p['issues'])}\n")
            
        f.write("\n## Duplicate Plugins\n")
        for d in duplicates[:50]:
            f.write(f"- **{d['name']}** in {d['file']}\n")

if __name__ == "__main__":
    main()
