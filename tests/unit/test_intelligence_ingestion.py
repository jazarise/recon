import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from reconx.core.intelligence.schemas import AssetSchema
from reconx.core.intelligence.intelligence_store import IntelligenceStore
from pydantic import ValidationError

def test_asset_schema_valid():
    asset = AssetSchema(asset_type="DOMAIN", value="example.com", project_id="test")
    assert asset.value == "example.com"
    
    asset_ip = AssetSchema(asset_type="IP", value="192.168.1.1", project_id="test")
    assert asset_ip.value == "192.168.1.1"

def test_asset_schema_invalid():
    with pytest.raises(ValidationError):
        AssetSchema(asset_type="DOMAIN", value="../evil", project_id="test")
        
    with pytest.raises(ValidationError):
        AssetSchema(asset_type="IP", value="300.300.300.300", project_id="test")

@pytest.mark.asyncio
async def test_intelligence_store_deduplication():
    mock_db = AsyncMock()
    mock_res = MagicMock()
    mock_res.scalars().first.return_value = None
    mock_res.scalars().all.return_value = []
    mock_db.execute.return_value = mock_res
    
    store = IntelligenceStore(mock_db)
    
    results = {
        "assets": [
            {"type": "DOMAIN", "value": "example.com", "source": "tool1"},
            {"type": "DOMAIN", "value": "example.com", "source": "tool2"}, # Duplicate
            {"type": "IP", "value": "8.8.8.8", "source": "tool1"},
            {"type": "DOMAIN", "value": "../../../etc/passwd"} # Invalid
        ],
        "findings": []
    }
    
    await store.ingest_plugin_result("proj_1", results)
    
    # Check that db.add was called for 'example.com' and '8.8.8.8', but not for the duplicate or invalid
    # It should be called 2 times for assets, and 2 times for history = 4 times total
    assert mock_db.add.call_count == 4
    
