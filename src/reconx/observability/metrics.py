from prometheus_client import Counter, Histogram, Gauge

# Counters
WORKFLOWS_TOTAL = Counter(
    "reconx_workflows_total", "Total number of workflows executed", ["status"]
)
PLUGINS_TOTAL = Counter(
    "reconx_plugins_total", "Total number of plugins executed", ["plugin", "status"]
)
ERRORS_TOTAL = Counter(
    "reconx_errors_total", "Total number of errors encountered", ["type"]
)
API_REQUESTS_TOTAL = Counter(
    "reconx_api_requests_total", "Total API requests", ["method", "endpoint", "status"]
)

# Histograms
WORKFLOW_DURATION = Histogram(
    "reconx_workflow_duration_seconds", "Duration of workflow execution"
)
API_REQUEST_DURATION = Histogram(
    "reconx_api_request_duration_seconds",
    "Duration of API requests",
    ["method", "endpoint"],
)
DB_LATENCY = Histogram(
    "reconx_db_latency_seconds", "Database query latency", ["operation"]
)

# Gauges
ACTIVE_WORKFLOWS = Gauge(
    "reconx_active_workflows", "Number of currently active workflows"
)
DB_CONNECTIONS = Gauge("reconx_db_connections", "Number of active database connections")
