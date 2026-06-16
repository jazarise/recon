from pathlib import Path

class WorkspaceManager:
    def __init__(self):
        self.active_workspace = "default"

    def set_workspace(self, name: str):
        self.active_workspace = name
        Path(f"workspaces/{name}").mkdir(parents=True, exist_ok=True)

    def list_workspaces(self):
        ws_dir = Path("workspaces")
        if not ws_dir.exists():
            return ["default"]
        return [d.name for d in ws_dir.iterdir() if d.is_dir()]
