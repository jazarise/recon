import pytest
from modules.osint.bigbountyrecon.plugin import Plugin
from core.models import Finding

def test_bigbountyrecon_execution():
    plugin = Plugin()
    target = "example.com"
    findings = plugin.execute(target, {})
    
    assert len(findings) > 0
    assert all(isinstance(f, Finding) for f in findings)
    assert findings[0].category == "osint_dork"
    assert findings[0].source == "bigbountyrecon"
    
    # Check that example.com is in the constructed URL
    assert "example.com" in findings[0].value
