import pytest
from unittest.mock import patch, MagicMock
from modules.osint.breach_check.plugin import Plugin
from core.models import Finding

@patch('requests.get')
def test_breach_check_execution(mock_get):
    # Mock leakcheck
    mock_resp1 = MagicMock()
    mock_resp1.status_code = 200
    mock_resp1.json.return_value = {"success": True, "sources": [{"name": "TestBreach"}]}
    
    # Mock hudsonrock
    mock_resp2 = MagicMock()
    mock_resp2.status_code = 200
    mock_resp2.json.return_value = {"stealers": [{"malware_path": "C:\\malware.exe"}]}
    
    mock_get.side_effect = [mock_resp1, mock_resp2]
    
    plugin = Plugin()
    findings = plugin.run("test@example.com")
    
    assert len(findings) == 2
    assert all(isinstance(f, Finding) for f in findings)
    assert findings[0].category == "data_breach"
    assert findings[0].source == "leakcheck"
    assert findings[1].category == "info_stealer"
    assert findings[1].source == "hudsonrock"
