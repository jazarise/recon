from plugins.web.gau import GauPlugin
from core.schemas import Endpoint, Parameter

def test_gau_plugin():
    plugin = GauPlugin()
    assert plugin.validate() == True
    results = plugin.run("example.com")
    normalized = plugin.normalize(results)
    assert isinstance(normalized, list)
    if normalized:
        has_ep = any(isinstance(i, Endpoint) for i in normalized)
        has_param = any(isinstance(i, Parameter) for i in normalized)
        assert has_ep
