from fastapi.testclient import TestClient
from reconx.api.main import app

client = TestClient(app)


def test_api_docs():
    response = client.get("/api/docs")
    assert response.status_code == 200


def test_api_openapi():
    response = client.get("/api/openapi.json")
    assert response.status_code == 200


def test_auth_router_unauthorized():
    response = client.get("/api/v1/users/me")
    assert response.status_code in [401, 403]


def test_reports_router_unauthorized():
    response = client.post("/api/v1/reports/generate", json={})
    assert response.status_code in [401, 403, 422]


def test_plugins_router_unauthorized():
    response = client.get("/api/v1/plugins")
    assert response.status_code in [401, 403]


def test_workflows_router_unauthorized():
    response = client.get("/api/v1/workflows")
    assert response.status_code in [401, 403]


def test_assets_router_unauthorized():
    response = client.get("/api/v1/assets")
    assert response.status_code in [401, 403]


def test_admin_router_unauthorized():
    response = client.get("/api/v1/admin/dashboard")
    assert response.status_code in [401, 403]
