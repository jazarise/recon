from fastapi import FastAPI
from reconx.api.routes import assets, reports, auth, plugins, users, workflows, admin
from reconx.observability.health import router as health_router
from reconx.observability.monitoring import router as monitoring_router
from reconx.observability.tracing import TracingMiddleware

app = FastAPI(
    title="ReconX API",
    version="3.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(TracingMiddleware)

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(admin.router, prefix="/api/v1", tags=["admin"])
app.include_router(assets.router, prefix="/api/v1", tags=["assets"])
app.include_router(reports.router, prefix="/api/v1", tags=["reports"])
app.include_router(plugins.router, prefix="/api/v1", tags=["plugins"])
app.include_router(workflows.router, prefix="/api/v1", tags=["workflows"])

app.include_router(health_router)
app.include_router(monitoring_router)
