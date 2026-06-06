"""ReconX — Projects API routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    target: str
    description: str = ""
    tags: List[str] = []


@router.get("/")
async def list_projects():
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    return {"projects": pm.list_projects()}


@router.post("/")
async def create_project(req: ProjectCreate):
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    try:
        proj = pm.create_project(req.name, req.target, req.description, req.tags)
        return {"status": "created", "project": proj}
    except FileExistsError:
        raise HTTPException(status_code=409, detail=f"Project '{req.name}' already exists")


@router.get("/{name}")
async def get_project(name: str):
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    proj = pm.get_project(name)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@router.delete("/{name}")
async def delete_project(name: str):
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    ok = pm.delete_project(name)
    if not ok:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "deleted"}
