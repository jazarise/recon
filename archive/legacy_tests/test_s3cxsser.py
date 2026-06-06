import pytest
from unittest.mock import patch, MagicMock
from modules.recon.s3cxsser.plugin import Plugin
from core.models import Finding

@patch('requests.get')
def test_s3cxsser_execution(mock_get):
    mock_resp = MagicMock()
    mock_resp.text = "<html><body>Welcome User123!</body></html>"
    mock_get.return_value = mock_resp
    
    plugin = Plugin()
    findings = plugin.run("http://example.com?name=User123&test=xyz")
    
    assert len(findings) == 1
    assert all(isinstance(f, Finding) for f in findings)
    assert findings[0].category == "reflected_parameter"
    assert "User123" in findings[0].value
