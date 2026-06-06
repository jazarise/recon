from fastapi import APIRouter
from core.orchestrator import orchestrator
import asyncio

router = APIRouter()

@router.get("/")
def get_scans():
    # In a real app we'd fetch from DB
    return [{"id": k, "target": v.target, "status": v.status} for k, v in orchestrator.running_scans.items()]

@router.post("/")
async def create_scan(target: str, workflow: str):
    # Async background task
    asyncio.create_task(orchestrator.run_workflow(workflow, target))
    return {"status": "started", "target": target, "workflow": workflow}
