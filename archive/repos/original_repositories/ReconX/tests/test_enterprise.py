import pytest
from core.database import DatabaseManager
from core.models import Asset, Service
from core.correlation_engine import CorrelationEngine
import asyncio

@pytest.fixture
def db_manager(tmp_path):
    import os
    os.environ["RECONX_DATA_DIR"] = str(tmp_path)
    # create a mock project workspace
    return DatabaseManager(project_name="test_project")

@pytest.mark.asyncio
async def test_correlation_engine(db_manager):
    engine = CorrelationEngine(db_manager)
    
    mock_workflow_results = {
        "target": "example.com",
        "workflow_id": "wf_123",
        "steps": [
            {
                "plugin": "dns_intelligence",
                "output": {
                    "subdomains": ["api.example.com", "dev.example.com"]
                }
            },
            {
                "plugin": "network_discovery",
                "output": {
                    "192.168.1.100": {
                        "ports": {"80": "open", "443": "open"}
                    }
                }
            }
        ]
    }
    
    # Run correlation
    await engine.correlate(mock_workflow_results)
    
    # Assert Database State
    session = db_manager.get_session()
    
    # Check Target Domain
    domain = session.query(Asset).filter_by(value="example.com").first()
    assert domain is not None
    assert domain.type == "domain"
    
    # Check Subdomains
    api = session.query(Asset).filter_by(value="api.example.com").first()
    assert api is not None
    assert api.type == "subdomain"
    
    # Check IP
    ip = session.query(Asset).filter_by(value="192.168.1.100").first()
    assert ip is not None
    assert ip.type == "ip"
    
    # Check Services
    services = session.query(Service).filter_by(asset_id=ip.id).all()
    assert len(services) == 2
    ports = [s.port for s in services]
    assert 80 in ports
    assert 443 in ports
    
    session.close()
