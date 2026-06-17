from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from reconx.core.database.session import get_db
from reconx.api.dependencies import require_operator, get_current_user
from reconx.core.database.models import User
from reconx.core.workflow.workflow_engine import workflow_engine
from reconx.core.workflow.state_manager import StateManager
from pydantic import BaseModel

router = APIRouter(prefix="/workflows", tags=["workflows"])


class WorkflowRunRequest(BaseModel):
    target: str


@router.get("")
async def list_workflows(current_user: User = Depends(get_current_user)):
    # Just list files in the workflow dir for simplicity
    import glob
    import os

    workflows = []
    for f in glob.glob("src/reconx/workflows/*.yaml"):
        workflows.append(os.path.basename(f).replace(".yaml", ""))
    return workflows


@router.post("/{name}/run")
async def run_workflow(
    name: str, req: WorkflowRunRequest, current_user: User = Depends(require_operator)
):
    try:
        result = await workflow_engine.execute_workflow(
            name, req.target, current_user.id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/executions/{id}")
async def get_execution(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    state_manager = StateManager(db)
    record = await state_manager.get_execution(id)
    if not record:
        raise HTTPException(status_code=404, detail="Execution not found")
    return record


@router.post("/executions/{id}/cancel")
async def cancel_execution(
    id: str,
    current_user: User = Depends(require_operator),
    db: AsyncSession = Depends(get_db),
):
    state_manager = StateManager(db)
    record = await state_manager.get_execution(id)
    if not record:
        raise HTTPException(status_code=404, detail="Execution not found")
    if record.status in ["SUCCESS", "FAILED", "CANCELLED"]:
        raise HTTPException(
            status_code=400, detail="Cannot cancel a completed workflow"
        )

    await state_manager.update_status(id, "CANCELLED")
    return {"message": "Workflow cancelled"}
