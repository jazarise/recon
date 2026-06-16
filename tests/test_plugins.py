def test_dns_enum_plugin():
    from src.reconx.plugins.dns_enum import Plugin
    import asyncio
    
    plugin = Plugin()
    result = asyncio.run(plugin.run("scanme.nmap.org"))
    assert "www.scanme.nmap.org" in result["subdomains"]

def test_guardrails():
    from src.reconx.core.guardrails import is_allowed
    assert is_allowed("scanme.nmap.org") == True
    
    try:
        is_allowed("google.com")
    except Exception as e:
        assert "not in the authorized scope" in str(e)
