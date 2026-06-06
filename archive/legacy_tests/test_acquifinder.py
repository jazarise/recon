import pytest
from modules.osint.acquifinder.plugin import Plugin
from core.models import Finding
import os

def test_acquifinder_execution():
    if "Apify_API_KEY" in os.environ:
        del os.environ["Apify_API_KEY"]
        
    plugin = Plugin()
    findings = plugin.run("Google")
    
    assert len(findings) > 0
    assert all(isinstance(f, Finding) for f in findings)
    assert findings[0].category == "acquisition"
    assert findings[0].source == "acquifinder"
    assert "Google acquires" in findings[0].value
