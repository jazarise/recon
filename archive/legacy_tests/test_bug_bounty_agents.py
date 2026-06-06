import pytest
from modules.ai.bug_bounty_agents.plugin import Plugin
from core.models import Finding

def test_bug_bounty_agents_execution():
    plugin = Plugin()
    findings = plugin.run("example.com")
    
    assert len(findings) > 0
    assert all(isinstance(f, Finding) for f in findings)
    assert findings[0].category == "ai_agent_prompt"
    assert findings[0].source == "bug_bounty_agents"
