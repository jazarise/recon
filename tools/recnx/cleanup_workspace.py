#!/usr/bin/env python3
"""
ReconX Final Workspace Cleanup Script
Relocates all legacy components, repositories, and outputs from e:/ReconX/
into e:/ReconX/archive/, leaving Reconx_V_2.0.0 as the sole active platform.
"""

import os
import shutil
from pathlib import Path

ROOT_DIR = Path("e:/ReconX")
ACTIVE_DIR = ROOT_DIR / "Reconx_V_2.0.0"
ARCHIVE_DIR = ROOT_DIR / "archive"

# Expected Archive Structure
ARCHIVE_PATHS = {
    "legacy_reconx": ARCHIVE_DIR / "legacy_reconx",
    "legacy_root": ARCHIVE_DIR / "legacy_reconx" / "root_files",
    "duplicate_repositories": ARCHIVE_DIR / "duplicate_repositories",
    "original_repositories": ARCHIVE_DIR / "original_repositories",
    "archived_plugins": ARCHIVE_DIR / "archived_plugins",
    "archived_workflows": ARCHIVE_DIR / "archived_workflows",
    "old_dashboards": ARCHIVE_DIR / "old_dashboards",
    "reports": ARCHIVE_DIR / "reports",
    "inventories": ARCHIVE_DIR / "inventories",
    "migration_logs": ARCHIVE_DIR / "migration_logs",
    "build_artifacts": ARCHIVE_DIR / "build_artifacts",
    "manifests": ARCHIVE_DIR / "manifests",
    "backups": ARCHIVE_DIR / "backups",
    "documentation": ARCHIVE_DIR / "documentation"
}

def setup_archive():
    print("[*] Creating archive hierarchy...")
    for path in ARCHIVE_PATHS.values():
        path.mkdir(parents=True, exist_ok=True)

def safe_move(src: Path, dst_dir: Path):
    """Move a file or directory safely to dst_dir."""
    if not src.exists():
        return False
    
    dst_path = dst_dir / src.name
    
    # Handle conflicts
    if dst_path.exists():
        if dst_path.is_dir():
            print(f"[-] Warning: Destination {dst_path} exists. Merging not implemented. Skipping {src.name}")
            return False
        else:
            dst_path = dst_dir / f"{src.name}.bak"
    
    try:
        shutil.move(str(src), str(dst_path))
        print(f"  [+] Moved: {src.name} -> {dst_dir.relative_to(ROOT_DIR)}")
        return True
    except Exception as e:
        print(f"  [!] Failed to move {src.name}: {e}")
        return False

def perform_cleanup():
    setup_archive()
    print("\n[*] Starting Relocation Process...")

    moved_count = 0
    
    # 1. Original Repositories
    repos_dir = ROOT_DIR / "Repos"
    if repos_dir.exists():
        print("\n[+] Relocating Repositories...")
        for item in repos_dir.iterdir():
            if item.is_dir():
                if safe_move(item, ARCHIVE_PATHS["original_repositories"]):
                    moved_count += 1
        # Also clean up the empty Repos directory itself
        try:
            shutil.rmtree(repos_dir)
            print("  [+] Removed empty Repos/ directory.")
        except:
            pass

    # 2. Legacy Dashboards & Workflows
    for item_name, dest_key in [("dashboard", "old_dashboards"), ("workflows", "archived_workflows")]:
        item = ROOT_DIR / item_name
        if item.exists():
            print(f"\n[+] Relocating legacy {item_name}...")
            if safe_move(item, ARCHIVE_PATHS[dest_key]):
                moved_count += 1

    # 3. Legacy ReconX Components
    legacy_components = ["core", "api", "events", "scripts", "tests"]
    print("\n[+] Relocating legacy codebase components...")
    for comp in legacy_components:
        item = ROOT_DIR / comp
        if item.exists():
            if safe_move(item, ARCHIVE_PATHS["legacy_reconx"]):
                moved_count += 1

    # 4. Reports & Inventories
    print("\n[+] Relocating reports and inventories...")
    inventories = ["repository_catalog.json", "duplicate_inventory.json", "feature_matrix.csv"]
    for inv in inventories:
        item = ROOT_DIR / inv
        if item.exists():
            if safe_move(item, ARCHIVE_PATHS["inventories"]):
                moved_count += 1
                
    reports = ["reconx_reports.txt", "DEPENDENCY_AUDIT.md", "audit"]
    for rep in reports:
        item = ROOT_DIR / rep
        if item.exists():
            if safe_move(item, ARCHIVE_PATHS["reports"]):
                moved_count += 1

    # 5. Logs & Outputs
    print("\n[+] Relocating build artifacts, logs, and outputs...")
    artifacts = ["logs", "outputs", "results"]
    for art in artifacts:
        item = ROOT_DIR / art
        if item.exists():
            if safe_move(item, ARCHIVE_PATHS["build_artifacts"]):
                moved_count += 1

    # 6. Documentation
    print("\n[+] Relocating documentation...")
    docs = ["docs", "SETUP.md"]
    for doc in docs:
        item = ROOT_DIR / doc
        if item.exists():
            if safe_move(item, ARCHIVE_PATHS["documentation"]):
                moved_count += 1

    # 7. Loose Root Files
    print("\n[+] Relocating loose root files...")
    loose_files = [".env.example", "config.yaml", "reconx.py", "requirements.txt", "smoke_test.py"]
    for lf in loose_files:
        item = ROOT_DIR / lf
        if item.exists():
            if safe_move(item, ARCHIVE_PATHS["legacy_root"]):
                moved_count += 1

    print(f"\n[*] Cleanup complete. Successfully relocated {moved_count} high-level items.")
    print("[*] The workspace e:/ReconX/ should now contain only 'Reconx_V_2.0.0' and 'archive'.")

if __name__ == "__main__":
    perform_cleanup()
