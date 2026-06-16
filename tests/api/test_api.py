import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_scans_get():
    response = client.get("/api/scans/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "scans" in data["data"]

def test_scans_post():
    response = client.post("/api/scans/", json={"target": "example.com", "workflow": "passive"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["target"] == "example.com"

def test_validation_error():
    response = client.post("/api/scans/", json={"target": "example.com"}) # Missing workflow
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert "errors" in data
