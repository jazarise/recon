def test_ai_prioritization():
    from src.reconx.ai.engine import IntelligenceEngine
    
    engine = IntelligenceEngine()
    
    mock_data = {
        "subdomains": ["admin.example.com", "cdn.example.com", "www.example.com"],
        "ports": [80, 22],
        "tech_stack": ["nginx"]
    }
    
    result = engine.process_raw_data("example.com", mock_data)
    
    assert "admin.example.com" in result["attack_surface"]["high_risk"]
    assert "cdn.example.com" in result["attack_surface"]["low_risk"]
    assert "Port 22" in result["attack_surface"]["high_risk"]
    assert len(result["recommendations"]) >= 2
