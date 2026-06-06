"""ReconX — Workflow API routes."""

from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import asyncio

router = APIRouter()


class WorkflowRequest(BaseModel):
    target: str
    profile: str = "basic"
    project: str = "default"


@router.post("/run")
async def run_workflow(req: WorkflowRequest, request: Request, background_tasks: BackgroundTasks):
    orchestrator = request.app.state.orchestrator
    profile_map = {
        "basic": "basic.yaml", "medium": "medium.yaml",
        "deep": "deep.yaml", "1": "basic.yaml", "2": "medium.yaml", "3": "deep.yaml",
    }
    wf_file = profile_map.get(req.profile, "basic.yaml")

    from core.paths import WORKFLOWS_DIR
    wf_path = str(WORKFLOWS_DIR / wf_file)

    result = await orchestrator.run_workflow(wf_path, req.target, project_name=req.project)
    return {"status": "completed", "workflow_id": result.get("workflow_id"), "result": result}


@router.get("/")
async def list_workflows(request: Request):
    from core.paths import WORKFLOWS_DIR
    workflows = []
    for wf in WORKFLOWS_DIR.glob("*.yaml"):
        import yaml
        with open(wf) as f:
            data = yaml.safe_load(f)
        workflows.append({
            "file": wf.name,
            "name": data.get("name", wf.stem),
            "description": data.get("description", ""),
            "mode": data.get("mode", "custom"),
            "steps": len(data.get("steps", data.get("stages", []))),
        })
    return {"workflows": workflows}
