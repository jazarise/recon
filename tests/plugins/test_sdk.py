import pytest
from sdk.plugin_base import BasePlugin
from core.models.finding import Finding

class DummyPlugin(BasePlugin):
    name = "Dummy"
    
    async def execute(self, target: str, **kwargs):
        return [Finding(category="Test", value="Pass")]

@pytest.mark.asyncio
async def test_base_plugin():
    plugin = DummyPlugin()
    assert plugin.name == "Dummy"
    results = await plugin.execute("example.com")
    assert len(results) == 1
    assert results[0].value == "Pass"
