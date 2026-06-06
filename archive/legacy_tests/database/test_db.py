from core.database.db import DatabaseManager
from core.schemas import OrganizationProfile, HostProfile, Vulnerability, Severity

def test_db_save_and_query():
    db = DatabaseManager(workspace="test_ws")
    org = OrganizationProfile(organization="TestOrg")
    host = HostProfile(domain="test.com")
    host.vulnerabilities.append(Vulnerability(category="XSS", severity=Severity.CRITICAL, url="test.com/v"))
    org.domains.append(host)
    
    db.save_organization(org)
    
    findings = db.query_findings(severity_filter="Critical")
    assert len(findings) == 1
    assert findings[0]["type"] == "XSS"
