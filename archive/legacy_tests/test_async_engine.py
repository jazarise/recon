import pytest
import asyncio
from reconx.core.async_engine import AsyncExecutor

@pytest.mark.asyncio
async def test_async_executor():
    executor = AsyncExecutor()
    
    async def dummy_task(value):
        await asyncio.sleep(0.1)
        return value * 2
        
    tasks = [dummy_task(1), dummy_task(2), dummy_task(3)]
    results = await executor.execute_all(tasks)
    
    assert set(results) == {2, 4, 6}
