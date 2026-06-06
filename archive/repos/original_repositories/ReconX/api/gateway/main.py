"""
ReconX Enterprise API Gateway — FastAPI application with lifecycle management,
CORS, WebSocket events, and all feature routes.
"""

from __future__ import annotations

import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

PROJECT_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from api.routes import agents, findings, tasks, workflows, reports, projects
from api.websocket.stream import router as ws_router, broadcast_event
from events.event_bus import EventBus
from core.workflow_engine import WorkflowEngine
from core.plugin_loader import PluginLoader
from core.execution_manager import ExecutionManager
from core.orchestrator import Orchestrator
from core.result_store import ResultStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    event_bus      = EventBus()
    plugin_loader  = PluginLoader()
    plugin_loader.discover_and_load()
    execution_mgr  = ExecutionManager(event_bus=event_bus, plugin_loader=plugin_loader)
    workflow_engine= WorkflowEngine(execution_manager=execution_mgr, event_bus=event_bus)
    result_store   = ResultStore()
    orchestrator   = Orchestrator(
        event_bus=event_bus,
        workflow_engine=workflow_engine,
        execution_manager=execution_mgr,
        result_store=result_store,
    )

    # Pipe all events → WebSocket broadcast
    WS_EVENTS = [
        "workflow.started", "step.started", "task.started",
        "task.completed", "task.failed", "step.completed",
        "workflow.completed", "orchestrator.started",
        "plugin_started", "plugin_completed", "plugin_failed",
    ]

    def make_handler(ename: str):
        async def handler(payload):
            await broadcast_event({"event": ename, "payload": payload})
        return handler

    for ename in WS_EVENTS:
        event_bus.subscribe(ename, make_handler(ename))

    app.state.orchestrator = orchestrator
    app.state.event_bus    = event_bus

    await orchestrator.start()
    yield


app = FastAPI(
    title="ReconX API",
    version="1.0.0",
    description="Unified Reconnaissance Orchestration Platform",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket
app.include_router(ws_router,            prefix="/ws",                      tags=["websocket"])

# REST API v1
app.include_router(workflows.router,     prefix="/api/v1/workflows",        tags=["workflows"])
app.include_router(tasks.router,         prefix="/api/v1/tasks",            tags=["tasks"])
app.include_router(findings.router,      prefix="/api/v1/findings",         tags=["findings"])
app.include_router(agents.router,        prefix="/api/v1/agents",           tags=["agents"])
app.include_router(reports.router,       prefix="/api/v1/reports",          tags=["reports"])
app.include_router(projects.router,      prefix="/api/v1/projects",         tags=["projects"])


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/api/v1/doctor")
def doctor():
    from core.doctor import Doctor
    doc = Doctor()
    checks = doc.run_all()
    summ   = doc.summary()
    return {"summary": summ, "checks": checks}


# ── Dashboard SPA (React build output) ───────────────────────────────────────
_DIST = Path(__file__).resolve().parent.parent.parent / "dashboard" / "dist"
_SPA_INDEX = _DIST / "index.html"

if _DIST.exists() and (_DIST / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(_DIST / "assets")), name="spa-assets")

async def _spa():
    if _SPA_INDEX.exists():
        return HTMLResponse(_SPA_INDEX.read_text(encoding="utf-8"))
    return HTMLResponse(_inline_dashboard())

app.add_api_route("/",         _spa, response_class=HTMLResponse, include_in_schema=False)
app.add_api_route("/dashboard", _spa, response_class=HTMLResponse, include_in_schema=False)
app.add_api_route("/projects",  _spa, response_class=HTMLResponse, include_in_schema=False)
app.add_api_route("/assets",    _spa, response_class=HTMLResponse, include_in_schema=False)
app.add_api_route("/reports",   _spa, response_class=HTMLResponse, include_in_schema=False)
app.add_api_route("/logs",      _spa, response_class=HTMLResponse, include_in_schema=False)
app.add_api_route("/settings",  _spa, response_class=HTMLResponse, include_in_schema=False)


def _inline_dashboard() -> str:
    """Minimal inline dashboard when external file is absent."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>ReconX Dashboard</title>
<style>
  body{background:#060a0f;color:#c8d8e8;font-family:'Segoe UI',sans-serif;margin:0;padding:0}
  .nav{background:#0c1420;border-bottom:1px solid #1a3050;padding:14px 32px;display:flex;align-items:center;gap:24px}
  .logo{font-size:22px;font-weight:700;color:#e53935;letter-spacing:4px}
  .nav a{color:#64b5f6;text-decoration:none;font-size:13px;padding:4px 12px;border-radius:4px}
  .nav a:hover{background:rgba(100,181,246,.1)}
  .main{max-width:1100px;margin:0 auto;padding:40px 24px}
  h1{font-size:28px;color:#e53935;margin-bottom:8px}
  .sub{color:#5a7a9a;margin-bottom:40px}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
  .card{background:#0c1420;border:1px solid #1a3050;border-radius:10px;padding:24px}
  .card-title{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#5a7a9a;margin-bottom:12px}
  .card-val{font-size:36px;font-weight:700;color:#64b5f6}
  .btn{display:inline-block;background:#e53935;color:#fff;padding:10px 24px;border-radius:6px;border:none;cursor:pointer;font-size:14px;font-weight:600;text-decoration:none;margin:4px}
  .btn:hover{background:#c62828}
  .btn-sec{background:#1a3050;color:#c8d8e8}
  .btn-sec:hover{background:#1e3a5f}
  table{width:100%;border-collapse:collapse;margin-top:12px;font-size:13px}
  th{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#5a7a9a;text-align:left;padding:8px 12px;border-bottom:1px solid #1a3050}
  td{padding:9px 12px;border-bottom:1px solid rgba(26,48,80,.4)}
  tr:last-child td{border-bottom:none}
  tr:hover td{background:rgba(229,57,53,.03)}
  #status{color:#30d158;font-size:12px;margin-left:auto}
  .scan-form{background:#0c1420;border:1px solid #1a3050;border-radius:10px;padding:24px;margin-bottom:28px}
  .scan-form h2{font-size:15px;color:#e53935;margin-bottom:18px;letter-spacing:1px}
  .form-row{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end}
  input,select{background:#111c2d;border:1px solid #1a3050;color:#c8d8e8;padding:8px 14px;border-radius:6px;font-size:13px;min-width:200px}
  input:focus,select:focus{outline:none;border-color:#e53935}
  #log{background:#111c2d;border:1px solid #1a3050;border-radius:6px;padding:16px;height:180px;overflow-y:auto;font-family:monospace;font-size:12px;color:#c8d8e8;margin-top:16px}
</style>
</head>
<body>
<div class="nav">
  <div class="logo">RECONX</div>
  <a href="#scan">Scan</a>
  <a href="#assets">Assets</a>
  <a href="#reports">Reports</a>
  <a href="/docs" target="_blank">API Docs</a>
  <span id="status">● Online</span>
</div>
<div class="main">
  <h1>ReconX Dashboard</h1>
  <p class="sub">Unified Reconnaissance Orchestration Platform · v1.0.0</p>

  <div class="grid" id="stats">
    <div class="card"><div class="card-title">Projects</div><div class="card-val" id="s-proj">—</div></div>
    <div class="card"><div class="card-title">Recent Jobs</div><div class="card-val" id="s-jobs">—</div></div>
    <div class="card"><div class="card-title">Reports</div><div class="card-val" id="s-reports">—</div></div>
    <div class="card"><div class="card-title">Agents Ready</div><div class="card-val" id="s-agents">—</div></div>
  </div>

  <div class="scan-form" id="scan">
    <h2>🚀 Launch Scan</h2>
    <div class="form-row">
      <input id="tgt" placeholder="Target (domain / IP)" />
      <input id="proj" placeholder="Project name" value="default"/>
      <select id="prof">
        <option value="basic">Basic</option>
        <option value="medium">Medium</option>
        <option value="deep">Deep</option>
      </select>
      <button class="btn" onclick="launchScan()">▶ Scan</button>
    </div>
    <div id="log">[ReconX] Ready. Enter a target and click Scan.</div>
  </div>

  <div class="card" style="margin-bottom:28px" id="assets">
    <div class="card-title">Recent Tasks</div>
    <table><thead><tr><th>Target</th><th>Status</th><th>Started</th><th>Steps</th></tr></thead>
    <tbody id="task-rows"><tr><td colspan="4" style="color:#5a7a9a;text-align:center;padding:20px">Loading…</td></tr></tbody>
    </table>
  </div>

  <div class="card" id="reports">
    <div class="card-title">Reports</div>
    <table><thead><tr><th>Filename</th><th>Format</th><th>Size</th></tr></thead>
    <tbody id="report-rows"><tr><td colspan="3" style="color:#5a7a9a;text-align:center;padding:20px">Loading…</td></tr></tbody>
    </table>
  </div>
</div>

<script>
const API = '/api/v1';
const log = document.getElementById('log');

function logMsg(msg) {
  const line = document.createElement('div');
  const ts = new Date().toLocaleTimeString();
  line.textContent = `[${ts}] ${msg}`;
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
}

async function fetchJSON(url) {
  const r = await fetch(url);
  return r.json();
}

async function loadStats() {
  try {
    const [projects, tasks, reports, agents] = await Promise.all([
      fetchJSON(`${API}/projects/`),
      fetchJSON(`${API}/tasks/`),
      fetchJSON(`${API}/reports/`),
      fetchJSON(`${API}/agents/`),
    ]);
    document.getElementById('s-proj').textContent    = projects.projects?.length ?? 0;
    document.getElementById('s-jobs').textContent    = tasks.count ?? 0;
    document.getElementById('s-reports').textContent = reports.count ?? 0;
    document.getElementById('s-agents').textContent  = agents.count ?? 0;

    const tb = document.getElementById('task-rows');
    const taskList = (tasks.tasks || []).slice(0,10);
    if (taskList.length === 0) {
      tb.innerHTML = '<tr><td colspan="4" style="color:#5a7a9a;text-align:center;padding:20px">No tasks yet</td></tr>';
    } else {
      tb.innerHTML = taskList.map(t => `<tr>
        <td>${t.target}</td>
        <td style="color:${t.status==='completed'?'#30d158':'#ffd60a'}">${t.status}</td>
        <td style="color:#5a7a9a">${(t.started_at||'').slice(0,16)}</td>
        <td>${t.step_count}</td>
      </tr>`).join('');
    }

    const rb = document.getElementById('report-rows');
    const repList = (reports.reports || []).filter(r=>r.format==='html').slice(0,10);
    if (repList.length === 0) {
      rb.innerHTML = '<tr><td colspan="3" style="color:#5a7a9a;text-align:center;padding:20px">No reports yet</td></tr>';
    } else {
      rb.innerHTML = repList.map(r => `<tr>
        <td style="color:#64b5f6">${r.filename}</td>
        <td>${r.format.toUpperCase()}</td>
        <td>${r.size_kb} KB</td>
      </tr>`).join('');
    }
  } catch(e) {
    console.error('Stats load error:', e);
  }
}

async function launchScan() {
  const target  = document.getElementById('tgt').value.trim();
  const project = document.getElementById('proj').value.trim() || 'default';
  const profile = document.getElementById('prof').value;
  if (!target) { logMsg('ERROR: Enter a target first.'); return; }
  logMsg(`Launching ${profile} scan on ${target} (project: ${project})…`);

  // WebSocket for live events
  const ws = new WebSocket(`ws://${location.host}/ws/events`);
  ws.onmessage = e => {
    try {
      const d = JSON.parse(e.data);
      const evt = d.event || 'event';
      const pl  = d.payload || {};
      if (pl.plugin)  logMsg(`${evt}: ${pl.plugin}${pl.error ? ' — ' + pl.error : ''}`);
      else if (pl.target) logMsg(`${evt}: ${pl.target}`);
    } catch(_) {}
  };
  ws.onerror = () => logMsg('WebSocket error — polling mode');

  try {
    const resp = await fetch(`${API}/workflows/run`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({target, profile, project}),
    });
    const data = await resp.json();
    logMsg(`Scan finished — status: ${data.status}  id: ${data.workflow_id}`);
    ws.close();
    await loadStats();
  } catch(e) {
    logMsg(`Scan error: ${e.message}`);
    ws.close();
  }
}

// Initial load + periodic refresh
loadStats();
setInterval(loadStats, 30000);

// WebSocket health
try {
  const ws = new WebSocket(`ws://${location.host}/ws/events`);
  ws.onopen  = () => document.getElementById('status').textContent = '● Live';
  ws.onclose = () => document.getElementById('status').textContent = '● Polling';
} catch(_) {}
</script>
</body>
</html>"""
