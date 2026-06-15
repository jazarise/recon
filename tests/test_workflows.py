import pytest
import os
from core.workflow_engine import workflow_engine
from core.orchestrator import orchestrator

def test_workflows_load():
    assert len(workflow_engine.workflows) > 0

def test_workflow_integrity():
    wname = list(workflow_engine.workflows.keys())[0]
    sorter, plugins = workflow_engine.build_execution_graph(wname)
    assert len(plugins) > 0

@pytest.mark.asyncio
async def test_orchestrator_run():
    wname = list(workflow_engine.workflows.keys())[0]
    context = await orchestrator.run_workflow(wname, "example.com")
    assert context.target == "example.com"
    assert isinstance(context.findings, list)
