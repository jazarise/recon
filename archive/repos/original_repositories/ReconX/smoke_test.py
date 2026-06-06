#!/usr/bin/env python3
"""
ReconX — Comprehensive smoke test.
Validates imports, module structure, workflow execution, project management,
doctor, and reporting pipeline.
"""

import sys
import asyncio
from pathlib import Path

ROOT = str(Path(__file__).resolve().parent)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

PASS = 0
FAIL = 0


def check(label: str, fn):
    global PASS, FAIL
    try:
        fn()
        print(f"  [PASS] {label}")
        PASS += 1
    except Exception as e:
        print(f"  [FAIL] {label}: {e}")
        FAIL += 1


def acheck(label: str, coro):
    """Run an async check."""
    global PASS, FAIL
    try:
        asyncio.run(coro)
        print(f"  [PASS] {label}")
        PASS += 1
    except Exception as e:
        print(f"  [FAIL] {label}: {e}")
        FAIL += 1


# ── Core imports ──────────────────────────────────────────────────────────────
print("\n[1/7] Core imports")
check("events.event_bus",              lambda: __import__("events.event_bus"))
check("core.workflow_engine",          lambda: __import__("core.workflow_engine"))
check("core.plugin_loader",            lambda: __import__("core.plugin_loader"))
check("core.execution_manager",        lambda: __import__("core.execution_manager"))
check("core.orchestrator",             lambda: __import__("core.orchestrator"))
check("core.result_store",             lambda: __import__("core.result_store"))
check("core.config",                   lambda: __import__("core.config"))
check("core.project_manager",          lambda: __import__("core.project_manager"))
check("core.doctor",                   lambda: __import__("core.doctor"))
check("core.correlation_engine",       lambda: __import__("core.correlation_engine"))
check("api.gateway.main (FastAPI app)",lambda: __import__("api.gateway.main"))

# ── Plugin loading ─────────────────────────────────────────────────────────────
print("\n[2/7] Plugin loading")
from core.plugin_loader import PluginLoader
pl = PluginLoader()
pl.discover_and_load()
for plugin in ["dns_intelligence", "network_discovery", "web_recon", "reporting", "llm_analysis"]:
    check(f"golden/{plugin}", lambda p=plugin: pl.get_plugin(p) or (_ for _ in ()).throw(ValueError(f"missing")))

# ── Doctor ───────────────────────────────────────────────────────────────────
print("\n[3/7] Doctor")
from core.doctor import Doctor
doc = Doctor()
checks = doc.run_all()
summ = doc.summary()
check("Doctor runs without crash",    lambda: None)
check("Doctor returns checks list",   lambda: len(checks) > 0 or (_ for _ in ()).throw(ValueError("empty")))
check("Doctor summary has passed key",lambda: "passed" in summ)
print(f"     Doctor: {summ['passed']} passed, {summ['failed']} failed, {summ['warned']} warned")

# ── Project manager ───────────────────────────────────────────────────────────
print("\n[4/7] Project manager")
from core.project_manager import ProjectManager
pm = ProjectManager()
TEST_PROJ = "__smoke_test_project__"

def _create_proj():
    pm.delete_project(TEST_PROJ)          # clean up any prior run
    proj = pm.create_project(TEST_PROJ, "scanme.nmap.org", "smoke test")
    assert proj["name"] == TEST_PROJ
    assert proj["target"] == "scanme.nmap.org"

def _list_proj():
    projects = pm.list_projects()
    names = [p["name"] for p in projects]
    assert TEST_PROJ in names

def _delete_proj():
    ok = pm.delete_project(TEST_PROJ)
    assert ok

check("Create project",  _create_proj)
check("List projects",   _list_proj)
check("Delete project",  _delete_proj)

# ── Workflow YAML files ───────────────────────────────────────────────────────
print("\n[5/7] Workflow files")
from core.workflow_engine import WorkflowEngine
from core.execution_manager import ExecutionManager
from events.event_bus import EventBus
eb = EventBus()
em = ExecutionManager(event_bus=eb, plugin_loader=pl)
we = WorkflowEngine(execution_manager=em, event_bus=eb)

for wf in ["basic.yaml", "medium.yaml", "deep.yaml"]:
    check(f"Load {wf}", lambda w=wf: we.load_workflow(f"workflows/{w}"))

# ── End-to-end basic workflow (localhost) ─────────────────────────────────────
print("\n[6/7] End-to-end basic workflow")

async def _e2e():
    from core.orchestrator import Orchestrator
    from core.result_store import ResultStore
    rs = ResultStore("__smoke_e2e__")
    orch = Orchestrator(event_bus=eb, workflow_engine=we,
                        execution_manager=em, result_store=rs)
    await orch.start()
    result = await orch.run_workflow("workflows/basic.yaml", "localhost", project_name="__smoke_e2e__")
    assert result["status"] == "completed", f"status={result['status']}"
    assert len(result["steps"]) >= 3, f"only {len(result['steps'])} steps"
    # Clean up
    pm.delete_project("__smoke_e2e__")

acheck("Basic workflow on localhost", _e2e())

# ── Reporting plugin standalone ───────────────────────────────────────────────
print("\n[7/7] Reporting plugin standalone")

async def _reporting():
    adapter = pl.get_plugin("reporting")
    assert adapter is not None
    ctx = {
        "target": "test.example.com",
        "network_discovery": {"open_ports": [80, 443], "services": [{"port": 80, "state": "open"}]},
        "web_recon": {"urls": ["http://test.example.com"], "technologies": ["nginx"]},
        "dns_intelligence": {"records": {"A": ["1.2.3.4"]}, "subdomains": []},
        "llm_analysis": {"risk_score": 25, "risk_level": "LOW",
                         "summary": "Test summary", "recommendations": [], "key_findings": []},
        "findings": [],
    }
    result = await adapter.execute({}, ctx)
    assert "reports" in result
    reports = result["reports"]
    for fmt in ["markdown", "json", "csv", "html"]:
        path = Path(reports[fmt])
        assert path.exists(), f"{fmt} report not created at {path}"

acheck("Reporting generates 4 formats", _reporting())

# ── Summary ───────────────────────────────────────────────────────────────────
total = PASS + FAIL
print(f"\n{'='*50}")
print(f"Smoke Test Results: {PASS}/{total} passed, {FAIL} failed")
print('='*50)
sys.exit(0 if FAIL == 0 else 1)
