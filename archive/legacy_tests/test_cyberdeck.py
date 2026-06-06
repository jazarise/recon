import pytest
from modules.recon.cyberdeck.plugin import Plugin
from core.models import Finding

def test_cyberdeck_execution():
    plugin = Plugin()
    findings = plugin.run("example.com")
    
    assert len(findings) > 0
    assert all(isinstance(f, Finding) for f in findings)
    assert findings[0].category == "cyberdeck_command"
    assert findings[0].source == "cyberdeck"
    
    # We copied commands.json, there should be at least a few hundred
    assert len(findings) > 100
