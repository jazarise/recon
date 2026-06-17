import pytest
import asyncio
from reconx.core.workflow.task import Task
from reconx.core.workflow.dependency_graph import DependencyGraph
from reconx.core.workflow.exceptions import DependencyCycleError
from reconx.core.workflow.scheduler import WorkflowScheduler
from reconx.core.workflow.execution_context import ExecutionContext
from reconx.core.workflow.result_aggregator import ResultAggregator


def test_dag_validation_no_cycles():
    tasks = [
        Task(id="1", plugin="test"),
        Task(id="2", plugin="test", depends_on=["1"]),
        Task(id="3", plugin="test", depends_on=["2"]),
    ]
    graph = DependencyGraph(tasks)
    assert len(graph.graph["1"]) == 1
    assert graph.graph["1"][0] == "2"


def test_dag_validation_with_cycles():
    tasks = [
        Task(id="1", plugin="test", depends_on=["3"]),
        Task(id="2", plugin="test", depends_on=["1"]),
        Task(id="3", plugin="test", depends_on=["2"]),
    ]
    with pytest.raises(DependencyCycleError):
        DependencyGraph(tasks)


@pytest.mark.asyncio
async def test_scheduler_execution_order(monkeypatch):
    executed = []

    # Mock execute_plugin instead of task execution directly so we test the scheduler logic properly.
    # Wait, the scheduler uses plugin_manager.execute_plugin. It's easier to mock scheduler.execute_task.

    tasks = [
        Task(id="1", plugin="test"),
        Task(id="2", plugin="test", depends_on=["1"]),
        Task(id="3", plugin="test", depends_on=["1"]),
    ]
    graph = DependencyGraph(tasks)
    context = ExecutionContext(workflow_id="test", target="test")
    aggregator = ResultAggregator()
    scheduler = WorkflowScheduler(graph, context, aggregator)

    async def mock_execute(task):
        executed.append(task.id)
        task.status = "SUCCESS"
        scheduler.completed.add(task.id)
        scheduler.running_tasks.remove(task.id)

    monkeypatch.setattr(scheduler, "execute_task", mock_execute)
    await scheduler.run()

    assert executed[0] == "1"
    assert set(executed[1:]) == {"2", "3"}


@pytest.mark.asyncio
async def test_parallel_execution(monkeypatch):
    tasks = [Task(id="1", plugin="test"), Task(id="2", plugin="test")]
    graph = DependencyGraph(tasks)
    context = ExecutionContext(workflow_id="test", target="test")
    aggregator = ResultAggregator()
    scheduler = WorkflowScheduler(graph, context, aggregator)

    running_concurrently = 0
    max_concurrent = 0

    async def mock_execute(task):
        nonlocal running_concurrently, max_concurrent
        running_concurrently += 1
        max_concurrent = max(max_concurrent, running_concurrently)
        await asyncio.sleep(0.1)
        task.status = "SUCCESS"
        scheduler.completed.add(task.id)
        running_concurrently -= 1
        scheduler.running_tasks.remove(task.id)

    monkeypatch.setattr(scheduler, "execute_task", mock_execute)
    await scheduler.run()

    assert max_concurrent == 2
