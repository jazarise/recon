from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from reconx.core.database.session import get_db
from reconx.api.dependencies import require_operator, get_current_user
from reconx.core.database.models import User, PluginExecution
from reconx.core.plugins.manager import plugin_manager
from pydantic import BaseModel

router = APIRouter(prefix="/plugins", tags=["plugins"])


class PluginExecuteRequest(BaseModel):
    target_id: str
    target_value: str


@router.get("", response_model=List[Dict[str, Any]])
async def list_plugins(current_user: User = Depends(get_current_user)):
    plugin_manager.load_all()
    return plugin_manager.list_plugins()


@router.get("/executions")
async def list_executions(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import select

    result = await db.execute(
        select(PluginExecution).order_by(PluginExecution.started_at.desc()).limit(100)
    )
    return result.scalars().all()


@router.get("/{name}")
async def get_plugin_details(name: str, current_user: User = Depends(get_current_user)):
    plugins = plugin_manager.list_plugins()
    for p in plugins:
        if p.get("name") == name:
            return p
    raise HTTPException(status_code=404, detail="Plugin not found")


@router.post("/{name}/execute")
async def execute_plugin(
    name: str,
    req: PluginExecuteRequest,
    current_user: User = Depends(require_operator),
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await plugin_manager.execute_plugin(
            db, name, req.target_id, req.target_value
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
