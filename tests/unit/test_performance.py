import pytest
import time
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_api_latency_performance():
    # Enforce API Response Latency thresholds
    start = time.perf_counter()
    response = client.get("/api/health")
    duration = time.perf_counter() - start
    assert response.status_code == 200
    assert duration < 0.1  # Requires API latency to fall strictly below 100ms in testing environments

def test_workflow_init_speed():
    # Enforce fast synchronous validation processing before task delegation
    start = time.perf_counter()
    response = client.post("/api/scans/", json={"target": "example.com", "workflow": "passive"})
    duration = time.perf_counter() - start
    assert response.status_code == 200
    assert duration < 0.2  # Requires validation initialization under 200ms
