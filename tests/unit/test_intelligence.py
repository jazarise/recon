from reconx.core.intelligence.asset_normalizer import AssetNormalizer
from reconx.core.intelligence.asset_correlator import AssetCorrelator


def test_asset_normalizer_ip():
    assert AssetNormalizer.validate_ip("192.168.1.1") == "192.168.1.1"
    assert AssetNormalizer.validate_ip("invalid_ip") is None


def test_asset_normalizer_domain():
    assert AssetNormalizer.normalize_domain(" Example.com. ") == "example.com"


def test_asset_normalizer_url():
    assert AssetNormalizer.normalize_url("example.com/api/") == "http://example.com/api"


def test_asset_correlator_basic():
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
