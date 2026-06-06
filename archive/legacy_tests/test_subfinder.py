from plugins.discovery.subfinder import SubfinderPlugin
from core.schemas import Domain

def test_subfinder_plugin_validate():
    plugin = SubfinderPlugin()
    assert plugin.validate() == True

def test_subfinder_plugin_run_and_normalize():
    plugin = SubfinderPlugin()
    results = plugin.run("example.com")
    normalized = plugin.normalize(results)
    assert isinstance(normalized, list)
    if normalized:
        assert isinstance(normalized[0], Domain)
