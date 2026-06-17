# API Reference

The ReconX REST API is built on FastAPI. It is fully asynchronous and self-documenting.
The complete OpenAPI schema can be explored interactively at `/api/docs` on your deployed instance.

## Authentication
All endpoints (except login/register) require a JWT Bearer token.

```http
POST /api/v1/auth/token
Content-Type: application/x-www-form-urlencoded

username=admin&password=SuperSecretPassword!
```

## Projects

### List Projects
```http
GET /api/v1/projects
Authorization: Bearer <TOKEN>
```
Response:
```json
[
  {
    "id": "1",
    "name": "External Recon",
    "status": "active"
  }
]
```

## Workflows

### Run a Workflow
```http
POST /api/v1/workflows/run
Authorization: Bearer <TOKEN>
Content-Type: application/json

{
  "project_id": "1",
  "workflow_name": "passive_recon",
  "target": "example.com"
}
```

## Assets

### List Assets
```http
GET /api/v1/assets?project_id=1
Authorization: Bearer <TOKEN>
```
