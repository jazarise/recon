from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from api.routes import projects, assets, scans, findings, reports, auth
import os

app = FastAPI(title="ReconX API", version="2.0.0", docs_url="/api/docs", openapi_url="/api/openapi.json")

# API Routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(assets.router, prefix="/api/assets", tags=["assets"])
app.include_router(scans.router, prefix="/api/scans", tags=["scans"])
app.include_router(findings.router, prefix="/api/findings", tags=["findings"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

from api.websocket import router as ws_router
app.include_router(ws_router, tags=["websocket"])

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# Static and Templates
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")
templates = Jinja2Templates(directory="dashboard/templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard_index(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)

@app.get("/overview", response_class=HTMLResponse)
async def overview_page(request: Request):
    return templates.TemplateResponse(name="overview.html", request=request)

@app.get("/scans", response_class=HTMLResponse)
async def scans_page(request: Request):
    return templates.TemplateResponse(name="scans.html", request=request)

@app.get("/findings", response_class=HTMLResponse)
async def findings_page(request: Request):
    return templates.TemplateResponse(name="findings.html", request=request)

@app.get("/workflows", response_class=HTMLResponse)
async def workflows_page(request: Request):
    return templates.TemplateResponse(name="workflows.html", request=request)
