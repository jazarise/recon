import pytest
from core.workflow_engine import WorkflowEngine, DependencyError

def test_workflow_engine_load():
    engine = WorkflowEngine(workflows_dir="workflows")
    assert "passive_recon" in engine.workflows
    assert "surface_mapping" in engine.workflows

def test_build_execution_graph():
    engine = WorkflowEngine(workflows_dir="workflows")
    sorter, plugins = engine.build_execution_graph("surface_mapping")
    
    assert "subfinder" in plugins
    assert "httpx" in plugins
    assert "katana" in plugins
    
    # We can prepare and get ready items to ensure order
    sorter.prepare()
    ready = sorter.get_ready()
    assert "subfinder" in ready
    
    sorter.done("subfinder")
    ready2 = sorter.get_ready()
    assert "httpx" in ready2
    
    sorter.done("httpx")
    ready3 = sorter.get_ready()
    assert "katana" in ready3
