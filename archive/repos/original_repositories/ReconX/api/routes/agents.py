"""ReconX — Agents API routes (plugin registry)."""

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def list_agents(request: Request):
    from core.plugin_loader import PluginLoader
    pl = PluginLoader()
    pl.discover_and_load()
    agents = []
    for name in pl.list_plugins():
        agents.append({"name": name, "status": "ready"})
    return {"count": len(agents), "agents": agents}
