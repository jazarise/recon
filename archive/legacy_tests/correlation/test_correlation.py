import pytest
from core.correlation.engine import correlation_engine
from core.correlation.rules import deduplicate_findings
from core.risk.engine import risk_engine
from core.database.models import DBFinding

def test_deduplication():
    f1 = DBFinding(category="vulnerability", value="XSS", source="app")
    f2 = DBFinding(category="vulnerability", value="XSS", source="app")
    f3 = DBFinding(category="port", value="80", source="app")
    
    findings = [f1, f2, f3]
    unique = deduplicate_findings(findings)
    assert len(unique) == 2

def test_risk_scoring():
    f1 = DBFinding(category="vulnerability", value="XSS", source="app")
    f1.severity = "high"
    
    f2 = DBFinding(category="vulnerability", value="SQLi", source="app")
    f2.severity = "critical"
    
    score = risk_engine.calculate_asset_risk([f1, f2])
    assert score == 100
    
    score_single = risk_engine.calculate_asset_risk([f1])
    assert score_single == 88
