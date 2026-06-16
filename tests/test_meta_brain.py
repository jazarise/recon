def test_meta_evolution():
    from src.reconx.meta.meta_brain import MetaDecisionEngine
    
    brain = MetaDecisionEngine()
    result = brain.run_self_reflection()
    
    # Assert that port_scan was disabled due to simulated 0% yield
    assert "port_scan" in result["disabled_plugins"]
    
    # Assert tech_detect was promoted in the evolutionary workflow
    assert result["new_workflow"][0] == "tech_detect"
