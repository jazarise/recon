import pytest
from reconx.plugins.loader import PluginManager
from reconx.integrations.nmap import NmapPlugin

def test_plugin_discovery():
    loader = PluginManager()
    plugins = loader.load_plugins()
    assert "nmap" in plugins
    assert "subfinder" in plugins

@pytest.mark.asyncio
async def test_nmap_plugin():
    plugin = NmapPlugin()
    assert plugin.name == "nmap"
    # Note: validation might fail depending on environment, we just test if the method exists
    valid = await plugin.validate()
    assert isinstance(valid, bool)
