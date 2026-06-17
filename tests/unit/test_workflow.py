import pytest
from reconx.core.workflow.dependency_graph import DependencyGraph
from reconx.core.workflow.task import Task
from reconx.core.workflow.workflow_engine import WorkflowEngine


def test_dependency_graph():
    t1 = Task(id="t1", plugin="test1")
    t2 = Task(id="t2", plugin="test2", depends_on=["t1"])
    t3 = Task(id="t3", plugin="test3", depends_on=["t1"])

    graph = DependencyGraph([t1, t2, t3])
    ready = graph.get_ready_tasks(set(), set())
    assert len(ready) == 1
    assert ready[0].id == "t1"


def test_dependency_graph_cycle():
    t1 = Task(id="t1", plugin="test1", depends_on=["t2"])
    t2 = Task(id="t2", plugin="test2", depends_on=["t1"])

    with pytest.raises(Exception):
        DependencyGraph([t1, t2])


@pytest.mark.asyncio
async def test_workflow_engine_basic():
    engine = WorkflowEngine()
    assert engine is not None
