"""ReconX — Tasks/Jobs API routes."""

from fastapi import APIRouter
from core.paths import OUTPUTS_DIR
import json

router = APIRouter()


@router.get("/")
async def list_tasks():
    tasks = []
    for f in sorted(OUTPUTS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:50]:
        try:
            with open(f) as fh:
                d = json.load(fh)
            tasks.append({
                "workflow_id": d.get("workflow_id", f.stem),
                "target": d.get("target", "?"),
                "status": d.get("status", "?"),
                "started_at": d.get("started_at"),
                "completed_at": d.get("completed_at"),
                "step_count": len(d.get("steps", [])),
            })
        except Exception:
            pass
    return {"count": len(tasks), "tasks": tasks}
