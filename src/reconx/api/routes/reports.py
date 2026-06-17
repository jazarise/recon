from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from reconx.core.database.session import get_db
from reconx.api.dependencies import get_current_user
from reconx.core.database.models import User
from reconx.reporting.report_engine import ReportEngine
from reconx.reporting.dashboard_service import DashboardService

router = APIRouter()


@router.post("/reports/generate")
async def generate_report(
    format: str = "json",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    engine = ReportEngine(db)
    try:
        path = await engine.export_report(format)
        return {"status": "success", "path": path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/dashboard")
async def dashboard_summary(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    service = DashboardService(db)
    return await service.get_metrics()
