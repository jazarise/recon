def test_dns_enum_plugin():
    from reconx.plugins.dns_enum import Plugin
    import asyncio
    
    plugin = Plugin()
    result = asyncio.run(plugin.run("scanme.nmap.org"))
    assert "www.scanme.nmap.org" in result["subdomains"]

def test_guardrails():
    from reconx.core.guardrails import ScopeEnforcer
    assert ScopeEnforcer.validate_target("scanme.nmap.org") == True
    
    try:
        ScopeEnforcer.validate_target("google.com")
    except Exception as e:
        assert "not in the authorized scope" in str(e)
