# ReconX Monitoring & Observability

## Endpoints

- `/health/live`: Returns `200 OK` if the web service is responding. Use this for Kubernetes liveness probes.
- `/health/ready`: Returns `200 OK` if the web service has established a database connection. Use this for readiness probes.
- `/metrics`: Exposes Prometheus metrics including workflow duration, error counts, and database latency.

## Key Metrics

| Metric Name | Type | Description |
|---|---|---|
| `reconx_workflows_total` | Counter | Total number of workflows executed. Labeled by `status` |
| `reconx_plugins_total` | Counter | Total number of plugin runs. Labeled by `plugin` and `status` |
| `reconx_errors_total` | Counter | Total exceptions caught. Labeled by `type` |
| `reconx_api_request_duration_seconds` | Histogram | Request latency. Labeled by `method` and `endpoint` |

## Distributed Tracing
ReconX injects an `X-Trace-Id` into API responses to correlate logs and actions across a single API request flow.
