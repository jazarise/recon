import os
import shutil
from pathlib import Path

def setup_v2_architecture():
    workspace = Path("e:/ReconX")
    v2_root = workspace / "Reconx_V_2.0.0"
    
    # Create required directories
    dirs = [
        "core", "modules", "plugins", "workflows", "dashboard",
        "api", "intelligence", "integrations", "reports",
        "config", "cli", "docs", "tests", "setup", "installers",
        "tools/recnx"
    ]
    
    for d in dirs:
        (v2_root / d).mkdir(parents=True, exist_ok=True)
    
    # Also create the archive deprecated path
    (workspace / "archive" / "deprecated").mkdir(parents=True, exist_ok=True)
    
    print("[+] V2.0.0 Directory structure created.")
    
    # Copy from canonical source
    source_root = workspace / "ReconX"
    if not source_root.exists():
        print("[-] Primary Core not found at ReconX!")
        return
        
    mappings = {
        "core": "core",
        "api": "api",
        "cli": "cli",
        "workflows": "workflows",
        "docs": "docs",
        "tests": "tests",
        "intelligence": "intelligence",
        "events": "core/events", # Let's put events inside core as it's the engine
        "analysis": "intelligence/analysis",
        "ai": "intelligence/ai",
        "reconx": "core/reconx", # The internal package
    }
    
    for src, dst in mappings.items():
        src_path = source_root / src
        dst_path = v2_root / dst
        if src_path.exists():
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            print(f"[+] Migrated {src} -> {dst}")
    
    # Copy standalone files
    files = ["reconx.py", "config.yaml", "requirements.txt", "README.md", "smoke_test.py"]
    for f in files:
        src_file = source_root / f
        if src_file.exists():
            shutil.copy2(src_file, v2_root / f)
            print(f"[+] Copied {f}")

    # For the dashboard, check which one has more files to find the 'most complete'
    dash_candidates = [
        workspace / "dashboard",
        workspace / "ReconX" / "dashboard",
        workspace / "ReconX_Final_v1.0.0" / "ReconX" / "dashboard"
    ]
    
    best_dash = None
    max_size = -1
    for c in dash_candidates:
        if c.exists():
            size = sum(f.stat().st_size for f in c.rglob('*') if f.is_file())
            if size > max_size:
                max_size = size
                best_dash = c
                
    if best_dash:
        print(f"[*] Selected dashboard from: {best_dash}")
        shutil.copytree(best_dash, v2_root / "dashboard", dirs_exist_ok=True)
        print("[+] Dashboard integrated.")
        
if __name__ == "__main__":
    setup_v2_architecture()
