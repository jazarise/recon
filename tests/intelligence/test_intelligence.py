from reconx.core.intelligence.asset_normalizer import AssetNormalizer
from reconx.core.intelligence.deduplicator import Deduplicator
from reconx.core.intelligence.relationship_engine import RelationshipEngine
from reconx.core.intelligence.asset_correlator import AssetCorrelator
from reconx.core.intelligence.risk_scoring import RiskScoring


def test_asset_normalizer():
    # Mixed-case domains normalize correctly
    assert AssetNormalizer.normalize_domain("API.Example.com.") == "api.example.com"
    # URLs normalize correctly
    assert (
        AssetNormalizer.normalize_url("HTTPS://API.EXAMPLE.COM/")
        == "https://api.example.com"
    )
    assert AssetNormalizer.normalize_url("api.example.com") == "http://api.example.com"
    # IPs
    assert AssetNormalizer.validate_ip("192.168.1.1") == "192.168.1.1"
    assert AssetNormalizer.validate_ip("invalid") is None
    # Security
    assert not AssetNormalizer.is_safe_value("../../../etc/passwd")
    assert not AssetNormalizer.is_safe_value("javascript:alert(1)")
    assert AssetNormalizer.is_safe_value("api.example.com")


def test_deduplicator():
    assets = [
        {"asset_type": "DOMAIN", "value": "example.com"},
        {"asset_type": "DOMAIN", "value": "example.com"},
        {"asset_type": "URL", "value": "https://example.com"},
    ]
    deduped = Deduplicator.deduplicate_assets(assets)
    assert len(deduped) == 2


def test_relationship_engine():
    assets = [
        {"asset_type": "DOMAIN", "value": "example.com"},
        {"asset_type": "SUBDOMAIN", "value": "api.example.com"},
        {"asset_type": "SUBDOMAIN", "value": "dev.example.com"},
    ]
    rels = RelationshipEngine.infer_parent_child(assets)
    assert len(rels) == 2
    assert rels[0]["relationship_type"] == "subdomain_of"
    assert rels[0]["parent_value"] == "example.com"


def test_asset_correlator():
    findings = [
        {
            "title": "XSS",
            "severity": "HIGH",
            "asset_value": "example.com",
            "source": "nuclei",
        },
        {
            "title": "XSS",
            "severity": "HIGH",
            "asset_value": "example.com",
            "source": "dalfox",
        },
    ]
    correlated = AssetCorrelator.correlate_findings(findings)
    assert len(correlated) == 1
    assert "nuclei" in correlated[0]["sources"]
    assert "dalfox" in correlated[0]["sources"]


def test_risk_scoring():
    findings = [{"severity": "CRITICAL"}, {"severity": "HIGH"}, {"severity": "INFO"}]
    score = RiskScoring.calculate_project_score(findings)
    assert score == 18  # 10 + 7 + 1
