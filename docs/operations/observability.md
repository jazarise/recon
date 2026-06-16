# Observability Maturity

- **Metrics:** Exported to `/metrics` via Prometheus formatting.
- **Logs:** Structured JSON emitted to `stdout` captured by Fluentd -> ELK.
- **Traces:** OpenTelemetry wrapping SQL queries and HTTP plugin requests.
