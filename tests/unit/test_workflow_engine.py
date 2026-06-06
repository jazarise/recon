import pytest
from core.workflow_engine import WorkflowEngine, WorkflowContext

@pytest.fixture
def engine():
    return WorkflowEngine(workflows_dir="workflows")

def test_workflow_engine_init(engine):
    assert engine is not None
    assert isinstance(engine.workflows, dict)

def test_workflow_context():
    context = WorkflowContext(target="example.com", scan_id="1234")
    assert context.target == "example.com"
    assert context.scan_id == "1234"
    assert context.findings == []
