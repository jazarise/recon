"""ReconX — Findings API routes."""

from fastapi import APIRouter, Request, Query
from typing import Optional

router = APIRouter()


@router.get("/")
async def get_findings(
    project: str = Query(default="default"),
    asset_type: Optional[str] = None,
    limit: int = 100,
):
    from core.database import DatabaseManager
    from core.models import Asset, Service
    db_mgr = DatabaseManager(project)
    db = db_mgr.get_session()
    try:
        q = db.query(Asset)
        if asset_type:
            q = q.filter(Asset.type == asset_type)
        assets = q.limit(limit).all()
        result = []
        for a in assets:
            result.append({
                "id": a.id,
                "type": a.type,
                "value": a.value,
                "tags": a.tags or [],
                "first_seen": a.first_seen.isoformat() if a.first_seen else None,
            })
        return {"project": project, "count": len(result), "assets": result}
    finally:
        db.close()
