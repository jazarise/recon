from core.engine.ai_engine import AIEngine
from core.schemas import OrganizationProfile, HostProfile, Vulnerability, Severity

def test_ai_engine_correlation():
    org = OrganizationProfile(organization="TestOrg")
    host = HostProfile(domain="test.com")
    host.vulnerabilities.append(Vulnerability(category="XSS", severity=Severity.HIGH, url="test.com/v"))
    org.domains.append(host)
    
    engine = AIEngine()
    enriched = engine.process_organization(org)
    
    assert enriched.ai_executive_summary is not None
    assert enriched.ai_technical_summary is not None
    assert len(enriched.ai_technical_summary.correlated_findings) == 1
    assert enriched.ai_technical_summary.correlated_findings[0].risk.severity == Severity.HIGH
