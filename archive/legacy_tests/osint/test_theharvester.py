from plugins.osint.theharvester import TheHarvesterPlugin
from core.schemas import Email, Confidence

def test_theharvester_plugin():
    plugin = TheHarvesterPlugin()
    assert plugin.validate() == True
    results = plugin.run("example.com")
    normalized = plugin.normalize(results)
    assert isinstance(normalized, list)
    if normalized:
        assert isinstance(normalized[0], Email)
        assert normalized[0].confidence == Confidence.HIGH
