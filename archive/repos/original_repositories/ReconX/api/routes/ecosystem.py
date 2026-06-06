"""ReconX — Ecosystem/Plugin discovery route."""
from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def ecosystem():
    from core.plugin_loader import PluginLoader
    pl = PluginLoader()
    pl.discover_and_load()
    return {
        "plugins": pl.list_plugins(),
        "total": len(pl.list_plugins()),
    }
