import pytest
import asyncio
from unittest.mock import MagicMock, patch
from reconx.core.workflow.task import Task, TaskStatus
from reconx.core.workflow.dependency_graph import DependencyGraph
from reconx.core.workflow.result_aggregator import ResultAggregator
from reconx.core.workflow.execution_context import ExecutionContext
from reconx.core.workflow.scheduler import WorkflowScheduler
from reconx.core.plugins.base import PluginResult

@pytest.mark.asyncio
async def test_scheduler_timeout():
    # Setup
    task = Task(id="t1", plugin="slow_plugin", timeout=1)
    graph = DependencyGraph([task])
    context = ExecutionContext(workflow_id="w1", target="example.com", user="test")
    aggregator = ResultAggregator()
    
    scheduler = WorkflowScheduler(graph, context, aggregator)
    
    # Mock plugin manager to sleep for 2 seconds (longer than timeout of 1)
    async def mock_execute(*args, **kwargs):
        await asyncio.sleep(2)
        return PluginResult(status="success")
        
    with patch("reconx.core.workflow.scheduler.plugin_manager.execute_plugin", new=mock_execute):
        # We also need to mock async_session_factory
        class MockDB:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
            
        with patch("reconx.core.workflow.scheduler.async_session_factory", return_value=MockDB()):
            await scheduler.run()
            
    assert task.status == TaskStatus.FAILED
    assert "timed out" in task.error

@pytest.mark.asyncio
async def test_scheduler_task_isolation():
    t1 = Task(id="t1", plugin="fail_plugin")
    t2 = Task(id="t2", plugin="success_plugin") # Independent
    
    graph = DependencyGraph([t1, t2])
    context = ExecutionContext(workflow_id="w1", target="example.com", user="test")
    aggregator = ResultAggregator()
    
    scheduler = WorkflowScheduler(graph, context, aggregator)
    
    async def mock_execute(db, plugin_name, target_type, target):
        if plugin_name == "fail_plugin":
            raise ValueError("Boom")
        return PluginResult(status="success")
        
    with patch("reconx.core.workflow.scheduler.plugin_manager.execute_plugin", new=mock_execute):
        class MockDB:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
            
        with patch("reconx.core.workflow.scheduler.async_session_factory", return_value=MockDB()):
            await scheduler.run()
            
    assert t1.status == TaskStatus.FAILED
    assert t2.status == TaskStatus.SUCCESS
