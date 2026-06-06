import json
from pathlib import Path
from datetime import datetime
from core.database import DatabaseManager
from core.models import ScanHistory
from core.paths import OUTPUTS_DIR

class ResultStore:
    def __init__(self, project_name: str = "default"):
        self.project_name = project_name
        self.db_manager = DatabaseManager(project_name)
        
        # Legacy/File-based outputs fallback
        self.outputs_dir = self.db_manager.project_dir / "outputs"
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

    async def save_result(self, workflow_id: str, result_data: dict):
        # Save to filesystem
        file_path = self.outputs_dir / f"{workflow_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=2, default=str)
            
        # Save to database
        db = self.db_manager.get_session()
        try:
            started = result_data.get("started_at")
            if started:
                started = datetime.fromisoformat(started.replace("Z", "+00:00"))
                
            completed = result_data.get("completed_at")
            if completed:
                completed = datetime.fromisoformat(completed.replace("Z", "+00:00"))
                
            history = ScanHistory(
                workflow_id=workflow_id,
                target=result_data.get("target", "unknown"),
                mode=result_data.get("workflow_name", "unknown"),
                status=result_data.get("status", "completed"),
                started_at=started,
                completed_at=completed,
                raw_results=result_data
            )
            db.add(history)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Failed to save to DB: {e}")
        finally:
            db.close()

    async def get_result(self, workflow_id: str) -> dict:
        file_path = self.outputs_dir / f"{workflow_id}.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
