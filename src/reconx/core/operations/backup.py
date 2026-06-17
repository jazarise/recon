import shutil
from pathlib import Path
from datetime import datetime


class BackupManager:
    def __init__(self, workspace="default"):
        self.workspace = workspace

    def create_backup(self):
        ws_dir = Path(f"workspaces/{self.workspace}")
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = backup_dir / f"backup_{self.workspace}_{timestamp}"

        if ws_dir.exists():
            shutil.make_archive(str(archive_name), "zip", str(ws_dir))
            return f"{archive_name}.zip"
        return None

    def restore_backup(self, archive_path: str):
        pass
