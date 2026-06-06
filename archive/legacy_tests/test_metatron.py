import pytest
from unittest.mock import patch, MagicMock
from modules.osint.metatron.plugin import Plugin
from core.models import Finding

@patch('subprocess.run')
def test_metatron_execution(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = "Mocked output"
    mock_result.stderr = ""
    mock_run.return_value = mock_result
    
    plugin = Plugin()
    findings = plugin.run("example.com")
    
    assert len(findings) == 9
    assert all(isinstance(f, Finding) for f in findings)
    assert findings[0].category == "metatron_recon"
    assert findings[0].source == "metatron"
    assert findings[0].value == "Mocked output"
    
    # Check that curl http constructed correctly
    # Finding 3 is curl_http based on insertion order
    assert findings[3].metadata["tool"] == "curl_http"
