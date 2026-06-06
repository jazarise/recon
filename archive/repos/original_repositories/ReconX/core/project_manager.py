"""
ReconX Project Manager — create, list, and manage reconnaissance projects.
Each project gets its own directory tree and SQLite database.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from core.paths import PROJECT_ROOT
from core.database import DatabaseManager
from core.logger import setup_logger

logger = setup_logger("ProjectManager")

PROJECTS_DIR = PROJECT_ROOT / "projects"


class ProjectManager:
    def __init__(self):
        PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

    def list_projects(self) -> List[Dict[str, Any]]:
        """Return list of all project dicts with metadata."""
        projects = []
        for p in sorted(PROJECTS_DIR.iterdir()):
            if p.is_dir():
                meta = self._load_meta(p)
                projects.append(meta)
        return projects

    def create_project(self, name: str, target: str, description: str = "", tags: List[str] = None) -> Dict[str, Any]:
        """Create a new project workspace and return its metadata."""
        safe_name = self._safe_name(name)
        project_dir = PROJECTS_DIR / safe_name

        if project_dir.exists():
            raise FileExistsError(f"Project '{safe_name}' already exists.")

        # Standard subdirectory layout per spec
        for subdir in ["raw", "processed", "reports", "screenshots", "logs", "graph", "metadata", "outputs"]:
            (project_dir / subdir).mkdir(parents=True, exist_ok=True)

        meta = {
            "name": safe_name,
            "display_name": name,
            "target": target,
            "description": description,
            "tags": tags or [],
            "created_at": datetime.utcnow().isoformat() + "Z",
            "last_scan": None,
            "scan_count": 0,
            "status": "new",
        }
        self._save_meta(project_dir, meta)

        # Initialize database
        DatabaseManager(safe_name)

        logger.info(f"Project created: {safe_name} → target: {target}")
        return meta

    def get_project(self, name: str) -> Optional[Dict[str, Any]]:
        """Load metadata for a project by name."""
        safe_name = self._safe_name(name)
        project_dir = PROJECTS_DIR / safe_name
        if not project_dir.exists():
            return None
        return self._load_meta(project_dir)

    def update_project_scan(self, name: str):
        """Bump scan count and update last_scan timestamp."""
        safe_name = self._safe_name(name)
        project_dir = PROJECTS_DIR / safe_name
        meta = self._load_meta(project_dir)
        meta["last_scan"] = datetime.utcnow().isoformat() + "Z"
        meta["scan_count"] = meta.get("scan_count", 0) + 1
        meta["status"] = "scanned"
        self._save_meta(project_dir, meta)

    def delete_project(self, name: str) -> bool:
        safe_name = self._safe_name(name)
        project_dir = PROJECTS_DIR / safe_name
        if project_dir.exists():
            shutil.rmtree(project_dir)
            return True
        return False

    def recent_projects(self, n: int = 5) -> List[Dict[str, Any]]:
        all_projects = self.list_projects()
        with_scan = [p for p in all_projects if p.get("last_scan")]
        without_scan = [p for p in all_projects if not p.get("last_scan")]
        sorted_p = sorted(with_scan, key=lambda x: x.get("last_scan", ""), reverse=True)
        return (sorted_p + without_scan)[:n]

    # ── helpers ──────────────────────────────────────────────────────────
    @staticmethod
    def _safe_name(name: str) -> str:
        return name.strip().lower().replace(" ", "_").replace("/", "_").replace("\\", "_")

    @staticmethod
    def _save_meta(project_dir: Path, meta: dict):
        with open(project_dir / "metadata" / "project.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

    @staticmethod
    def _load_meta(project_dir: Path) -> dict:
        meta_file = project_dir / "metadata" / "project.json"
        if meta_file.exists():
            with open(meta_file, "r", encoding="utf-8") as f:
                return json.load(f)
        # Legacy: directory exists but no meta yet
        return {
            "name": project_dir.name,
            "display_name": project_dir.name,
            "target": "unknown",
            "description": "",
            "tags": [],
            "created_at": None,
            "last_scan": None,
            "scan_count": 0,
            "status": "legacy",
        }
