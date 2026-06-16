def test_timeline_diffs():
    from src.reconx.global.timeline import TimelineEngine
    engine = TimelineEngine()
    
    # Time 1
    diffs_t1 = engine.detect_changes("example.com", ["Port 80"])
    assert len(diffs_t1) == 1
    assert "New endpoint" in diffs_t1[0]["event"]
    
    # Time 2
    diffs_t2 = engine.detect_changes("example.com", ["Port 80", "Port 443"])
    assert len(diffs_t2) == 1
    assert "443" in diffs_t2[0]["event"]
    
    # Time 3 (Closure)
    diffs_t3 = engine.detect_changes("example.com", ["Port 443"])
    assert len(diffs_t3) == 1
    assert "Endpoint closed: Port 80" in diffs_t3[0]["event"]
