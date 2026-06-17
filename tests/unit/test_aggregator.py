import pytest
import asyncio
from reconx.core.workflow.result_aggregator import ResultAggregator
from reconx.core.plugins.base import PluginResult

@pytest.mark.asyncio
async def test_aggregator_concurrency():
    aggregator = ResultAggregator()
    
    async def add_result_coro(task_id: int):
        result = PluginResult(
            status="success",
            assets=[{"type": "DOMAIN", "value": f"example{task_id}.com"}],
            findings=[],
            logs=[f"Task {task_id} completed"]
        )
        await aggregator.add_result(f"t{task_id}", result)
        
    tasks = [add_result_coro(i) for i in range(100)]
    await asyncio.gather(*tasks)
    
    summary = aggregator.get_summary()
    assert summary["total_assets"] == 100
    assert len(aggregator.logs) == 100
