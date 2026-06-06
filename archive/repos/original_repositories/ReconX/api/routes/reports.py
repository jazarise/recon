"""ReconX — Reports API routes."""

from fastapi import APIRouter, HTTPException
from pathlib import Path
from core.paths import OUTPUTS_DIR

router = APIRouter()


@router.get("/")
async def list_reports():
    reports = []
    for f in sorted(OUTPUTS_DIR.glob("report_*"), key=lambda p: p.stat().st_mtime, reverse=True):
        reports.append({
            "filename": f.name,
            "format": f.suffix.lstrip("."),
            "size_kb": round(f.stat().st_size / 1024, 1),
            "path": str(f),
        })
    return {"count": len(reports), "reports": reports}


@router.get("/{filename}")
async def get_report(filename: str):
    path = OUTPUTS_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    content = path.read_text(encoding="utf-8")
    return {"filename": filename, "content": content}
