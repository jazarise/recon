import os
import json
import csv
import hashlib
from pathlib import Path
from collections import defaultdict

WORKSPACE = Path("e:/ReconX")
REPOS_DIR = WORKSPACE / "Repos"
OUTPUTS_DIR = WORKSPACE

def get_file_hash(filepath):
    """Calculate SHA256 of a file for exact duplicate detection."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def build_duplicate_inventory():
    print("[*] Building duplicate inventory...")
    hash_map = defaultdict(list)
    # We only care about key directories to avoid scanning 68,000 files deeply if not needed, 
    # but let's scan all .py, .yaml, .js, .json in major folders.
    target_dirs = [
        WORKSPACE / "ReconX",
        WORKSPACE / "ReconX_Final_v1.0.0",
        WORKSPACE / "ReconX_Final_v1.0.0_with_dashboard",
        WORKSPACE / "plugins",
        WORKSPACE / "core",
        WORKSPACE / "api",
        WORKSPACE / "workflows",
        WORKSPACE / "dashboard"
    ]
    
    # Also add the root files
    root_files = [f for f in WORKSPACE.iterdir() if f.is_file()]
    for f in root_files:
        if f.suffix in ['.py', '.yaml', '.txt', '.md']:
            h = get_file_hash(f)
            if h: hash_map[h].append(str(f))

    for d in target_dirs:
        if not d.exists(): continue
        for root, _, files in os.walk(d):
            # Skip caches
            if '__pycache__' in root or 'node_modules' in root or '.git' in root:
                continue
            for file in files:
                if file.endswith(('.py', '.yaml', '.yml', '.js', '.ts', '.json', '.txt', '.md')):
                    path = Path(root) / file
                    h = get_file_hash(path)
                    if h:
                        hash_map[h].append(str(path))
    
    inventory = []
    for h, paths in hash_map.items():
        if len(paths) > 1:
            # Determine canonical candidate: prefer e:\ReconX\ReconX
            canonical = paths[0]
            for p in paths:
                if "ReconX\\ReconX\\" in p or "ReconX_Final_v1.0.0_with_dashboard" in p:
                    canonical = p
                    break
            
            inventory.append({
                "File": Path(paths[0]).name,
                "Location": paths,
                "Duplicate Count": len(paths),
                "Canonical Candidate": canonical
            })
    
    out_path = OUTPUTS_DIR / "duplicate_inventory.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=4)
    print(f"[+] Saved {out_path} ({len(inventory)} duplicated sets found)")

def analyze_repositories():
    print("[*] Analyzing repositories...")
    catalog = []
    
    if not REPOS_DIR.exists():
        print(f"[-] {REPOS_DIR} not found.")
        return catalog

    for repo in REPOS_DIR.iterdir():
        if not repo.is_dir(): continue
        
        # Determine language
        lang = "Unknown"
        has_py = any(repo.rglob("*.py"))
        has_go = any(repo.rglob("*.go"))
        has_js = any(repo.rglob("*.js"))
        has_sh = any(repo.rglob("*.sh"))
        
        if has_go: lang = "Go"
        elif has_py: lang = "Python"
        elif has_js: lang = "JavaScript/TypeScript"
        elif has_sh: lang = "Shell"
        
        # Classification guess
        classification = "REQUIRES_WRAPPER"
        if lang == "Python": classification = "DIRECTLY_USABLE"
        elif lang == "Unknown": classification = "ARCHIVE_ONLY"
        
        entrypoints = [str(f.relative_to(repo)) for f in repo.glob("*.py")] + \
                      [str(f.relative_to(repo)) for f in repo.glob("main.go")] + \
                      [str(f.relative_to(repo)) for f in repo.glob("*.sh")]
        
        catalog.append({
            "Repository Name": repo.name,
            "Purpose": "Security Tool / Recon / Automation",
            "Language": lang,
            "Dependencies": "requirements.txt/go.mod/package.json",
            "Entrypoints": entrypoints[:3], # Limit
            "Features": ["Reconnaissance", "Scanning"],
            "Reusable Components": ["CLI Interface", "Scanners"],
            "Integration Complexity": "Medium",
            "Migration Recommendation": f"Wrap using standard module adapter for {lang}",
            "Classification": classification
        })
        
    out_path = OUTPUTS_DIR / "repository_catalog.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=4)
    print(f"[+] Saved {out_path} ({len(catalog)} repositories analyzed)")
    return catalog

def generate_feature_matrix(catalog):
    print("[*] Generating feature matrix...")
    matrix_path = OUTPUTS_DIR / "feature_matrix.csv"
    with open(matrix_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Feature", "Source Repository", "Current Location", "Category", "Migration Target", "Priority", "Status"])
        
        # Add Core Features
        writer.writerow(["Workflow Engine", "ReconX Core", "ReconX/ReconX/core", "Orchestration", "Reconx_V_2.0.0/core", "High", "Pending"])
        writer.writerow(["Plugin Loader", "ReconX Core", "ReconX/ReconX/core", "Orchestration", "Reconx_V_2.0.0/core", "High", "Pending"])
        writer.writerow(["Dashboard UI", "ReconX_Final_v1.0.0_with_dashboard", "ReconX_Final_v1.0.0_with_dashboard", "UI", "Reconx_V_2.0.0/dashboard", "High", "Pending"])
        
        # Add Repo Features
        for repo in catalog:
            if repo["Classification"] != "ARCHIVE_ONLY":
                feature_name = f"{repo['Repository Name']} Integration"
                writer.writerow([feature_name, repo['Repository Name'], f"Repos/{repo['Repository Name']}", repo['Language'], f"Reconx_V_2.0.0/modules/{repo['Repository Name'].lower()}", "Medium", "Pending"])

    print(f"[+] Saved {matrix_path}")

if __name__ == "__main__":
    print("--- RECNX Analysis Tool ---")
    build_duplicate_inventory()
    catalog = analyze_repositories()
    generate_feature_matrix(catalog)
    print("--- Analysis Complete ---")
