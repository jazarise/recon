import pytest
from unittest.mock import patch, MagicMock
from modules.recon.deksterecon.plugin import Plugin
from core.models import Finding

@patch('subprocess.run')
def test_deksterecon_execution(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = "Mocked output"
    mock_result.stderr = ""
    mock_run.return_value = mock_result
    
    plugin = Plugin()
    findings = plugin.run("example.com")
    
    assert len(findings) == 6
    assert all(isinstance(f, Finding) for f in findings)
    assert findings[0].category == "deksterecon_result"
    assert findings[0].source == "deksterecon"
