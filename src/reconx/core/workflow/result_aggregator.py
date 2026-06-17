from typing import Dict, Any, List


import asyncio

class ResultAggregator:
    def __init__(self):
        self.assets: Dict[str, Dict[str, Any]] = {}
        self.findings: List[Dict[str, Any]] = []
        self.logs: List[str] = []
        self._lock = asyncio.Lock()

    async def add_result(self, task_id: str, result: Any):  # result is a PluginResult
        async with self._lock:
            for asset in result.assets:
                key = f"{asset.get('type')}:{asset.get('value')}"
                if key not in self.assets:
                    self.assets[key] = asset

            for finding in result.findings:
                finding["source_task"] = task_id
                self.findings.append(finding)

            for log in result.logs:
                self.logs.append(f"[{task_id}] {log}")

            for error in result.errors:
                self.logs.append(f"[{task_id}] ERROR: {error}")

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_assets": len(self.assets),
            "total_findings": len(self.findings),
            "unique_assets": list(self.assets.values()),
        }
