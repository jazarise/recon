import os
import shutil
import json
from pathlib import Path

def deduplicate_plugins():
    workspace = Path("e:/ReconX")
    v2_plugins = workspace / "Reconx_V_2.0.0" / "plugins"
    v2_plugins.mkdir(parents=True, exist_ok=True)
    
    # Sources of plugins (ordered by preference)
    sources = [
        workspace / "ReconX" / "plugins",
        workspace / "plugins",
        workspace / "ReconX_Final_v1.0.0" / "ReconX" / "plugins",
        workspace / "Repos" / "ReconX" / "plugins"
    ]
    
    seen_plugins = set()
    total_found = 0
    total_copied = 0
    
    print("[*] Starting plugin deduplication...")
    for src in sources:
        if not src.exists(): continue
        for category in src.iterdir():
            if not category.is_dir(): continue
            if category.name == "__pycache__": continue
            
            cat_dest = v2_plugins / category.name
            cat_dest.mkdir(exist_ok=True)
            
            for plugin in category.iterdir():
                if not plugin.is_dir() or plugin.name == "__pycache__": continue
                
                total_found += 1
                plugin_key = f"{category.name}/{plugin.name}"
                
                if plugin_key not in seen_plugins:
                    seen_plugins.add(plugin_key)
                    # We copy this one
                    shutil.copytree(plugin, cat_dest / plugin.name, dirs_exist_ok=True)
                    total_copied += 1

    print(f"[+] Total plugin references scanned: {total_found}")
    print(f"[+] Unique plugins consolidated: {total_copied}")
    
    # Build a simple Plugin Registry JSON
    registry = []
    for cat in v2_plugins.iterdir():
        if not cat.is_dir(): continue
        for p in cat.iterdir():
            if not p.is_dir(): continue
            
            manifest = p / "tool.yaml"
            if manifest.exists():
                registry.append({
                    "id": f"{cat.name}.{p.name}",
                    "path": str(p.relative_to(workspace / "Reconx_V_2.0.0")),
                    "category": cat.name,
                    "status": "healthy"
                })
                
    registry_file = workspace / "Reconx_V_2.0.0" / "core" / "plugin_registry.json"
    registry_file.parent.mkdir(parents=True, exist_ok=True)
    with open(registry_file, "w") as f:
        json.dump(registry, f, indent=4)
        
    print(f"[+] Plugin Registry built with {len(registry)} plugins.")

if __name__ == "__main__":
    deduplicate_plugins()
