import os
import shutil
from pathlib import Path

def archive_legacy():
    workspace = Path("e:/ReconX")
    archive_dir = workspace / "archive" / "deprecated"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    print("[*] Archiving legacy ReconX copies...")
    
    legacy_targets = [
        workspace / "ReconX",
        workspace / "ReconX_Final_v1.0.0",
        workspace / "ReconX_Final_v1.0.0_with_dashboard",
        workspace / "plugins",
        workspace / "pccc"
    ]
    
    archived_count = 0
    for target in legacy_targets:
        if target.exists() and target.is_dir():
            if target.name == "ReconX" and target.parent == workspace:
                # Can't move the entire e:\ReconX\ReconX folder right now if we are inside it or running from it, 
                # but we will move it logically into archive_dir.
                dest = archive_dir / target.name
                if not dest.exists():
                    shutil.move(str(target), str(dest))
                    archived_count += 1
                    print(f"[+] Archived {target.name}")
            else:
                dest = archive_dir / target.name
                if not dest.exists():
                    shutil.move(str(target), str(dest))
                    archived_count += 1
                    print(f"[+] Archived {target.name}")

    print(f"[+] Successfully archived {archived_count} redundant systems to {archive_dir}.")
    
if __name__ == "__main__":
    archive_legacy()
