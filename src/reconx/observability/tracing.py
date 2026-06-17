import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from reconx.observability.metrics import API_REQUESTS_TOTAL, API_REQUEST_DURATION


class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        # We could filter out some endpoints like /metrics and /health
        if request.url.path not in [
            "/metrics",
            "/health",
            "/health/live",
            "/health/ready",
        ]:
            API_REQUESTS_TOTAL.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code,
            ).inc()

            API_REQUEST_DURATION.labels(
                method=request.method, endpoint=request.url.path
            ).observe(process_time)

        response.headers["X-Trace-Id"] = trace_id
        return response
