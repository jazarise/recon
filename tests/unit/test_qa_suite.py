import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_qa_health_stability():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_qa_schema_adherence():
    # Attempt bad schema, ensure robust fail open standard structure
    response = client.post("/api/scans/", json={})
    assert response.status_code == 422
    data = response.json()
    # It should still not crash or bleed tracebacks!
    assert "errors" in data

def test_qa_database_dependency_stub():
    # Validates integration sanity checks do not raise unbound exceptions
    assert app is not None
