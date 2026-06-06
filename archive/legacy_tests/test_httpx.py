from plugins.web.httpx import HttpxPlugin
from core.schemas import URL

def test_httpx_plugin():
    plugin = HttpxPlugin()
    assert plugin.validate() == True
    results = plugin.run("example.com")
    normalized = plugin.normalize(results)
    assert isinstance(normalized, list)
    if normalized:
        assert isinstance(normalized[0], URL)
