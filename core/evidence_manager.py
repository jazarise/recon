from pathlib import Path

class EvidenceManager:
    def __init__(self, workspace="default"):
        self.base_dir = Path(f"workspaces/{workspace}/evidence")
        for subdir in ["scans", "screenshots", "requests", "responses", "findings"]:
            (self.base_dir / subdir).mkdir(parents=True, exist_ok=True)

    def save_screenshot(self, name: str, data: bytes) -> str:
        path = self.base_dir / "screenshots" / name
        with open(path, "wb") as f:
            f.write(data)
        return str(path)

    def save_http_log(self, name: str, request: str, response: str) -> str:
        path = self.base_dir / "requests" / f"{name}_req.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(request)
        return str(path)
