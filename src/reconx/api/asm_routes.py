from fastapi import APIRouter
from core.asm.timeline_engine import timeline_engine
from core.asm.target_manager import target_manager
from core.alerts.alert_system import alert_system
from typing import Dict, List

router = APIRouter(prefix="/api/asm", tags=["asm"])

@router.get("/targets")
def get_targets():
    return target_manager.get_all_targets()

@router.get("/timeline/{target}")
def get_timeline(target: str) -> List[Dict]:
    return timeline_engine.get_timeline(target)

@router.get("/alerts")
def get_alerts() -> List[Dict]:
    return alert_system.alerts
