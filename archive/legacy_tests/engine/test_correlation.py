from core.engine.correlation_engine import CorrelationEngine
from core.schemas import Domain, Port

def test_correlation_engine():
    engine = CorrelationEngine()
    engine.ingest([Domain(value="example.com")])
    engine.ingest([Port(number=80)])
    
    profiles = engine.get_profiles()
    assert len(profiles) == 1
    assert profiles[0].domain == "example.com"
    assert 80 in profiles[0].ports
