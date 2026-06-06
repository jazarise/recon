from plugins.vulnerabilities.dalfox import DalfoxPlugin
from core.schemas import Vulnerability

def test_dalfox_plugin():
    plugin = DalfoxPlugin()
    assert plugin.validate() == True
    results = plugin.run("example.com")
    normalized = plugin.normalize(results)
    assert isinstance(normalized, list)
    if normalized:
        assert isinstance(normalized[0], Vulnerability)
