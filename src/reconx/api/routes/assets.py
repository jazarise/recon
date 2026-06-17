from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from reconx.core.database.session import get_db
from reconx.api.dependencies import get_current_user
from reconx.core.database.models import User
from reconx.core.intelligence.intelligence_store import IntelligenceStore
from reconx.core.intelligence.risk_scoring import RiskScoring
from reconx.core.database.models import Finding
from sqlalchemy import select

router = APIRouter(tags=["intelligence"])


@router.get("/assets")
async def list_assets(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    store = IntelligenceStore(db)
    return await store.get_assets()


@router.get("/assets/{id}/graph")
async def get_asset_graph(
    id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    store = IntelligenceStore(db)
    return await store.get_asset_graph()


@router.get("/findings")
async def list_findings(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    res = await db.execute(select(Finding))
    return [
        {"id": f.id, "title": f.title, "severity": f.severity.name}
        for f in res.scalars().all()
    ]


@router.get("/risk")
async def risk_summary(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    res = await db.execute(select(Finding))
    findings = [{"severity": f.severity.name} for f in res.scalars().all()]
    score = RiskScoring.calculate_project_score(findings)
    return {"project_risk_score": score, "total_findings": len(findings)}
