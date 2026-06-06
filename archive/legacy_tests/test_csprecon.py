import pytest
from unittest.mock import patch, MagicMock
from modules.recon.csprecon.plugin import Plugin
from core.models import Finding

@patch('requests.get')
def test_csprecon_execution(mock_get):
    mock_resp = MagicMock()
    mock_resp.headers = {
        "Content-Security-Policy": "default-src 'self'; script-src https://cdn.example.com https://api.test.org 'unsafe-inline';"
    }
    mock_get.return_value = mock_resp
    
    plugin = Plugin()
    findings = plugin.run("example.com")
    
    assert len(findings) == 2
    assert all(isinstance(f, Finding) for f in findings)
    assert findings[0].category == "csp_domain"
    
    values = [f.value for f in findings]
    assert "cdn.example.com" in values
    assert "api.test.org" in values
