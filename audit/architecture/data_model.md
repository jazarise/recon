# Unified Data Model

## Finding Normalization
To prevent chaos, ReconX no longer permits tools to output arbitrary JSON/TXT formats directly to reports or the dashboard. All data must flow through the SQLAlchemy Data Models defined in `core/models.py`.

### Core Entities
Every piece of output must be mapped to one of the following structured objects:

1. **Asset**: `type` (domain, ip, asn, url), `value`, `first_seen`, `tags`
2. **Service**: `port`, `protocol`, `service_name`, `product`, `version`
3. **Vulnerability**: `name`, `severity`, `description`, `discovered_at`
4. **ScanHistory**: Tracks workflow executions and their completion status.

### Flow
`Tool Output -> Plugin Normalize() -> SQLAlchemy Object -> SQLite Database -> API -> Dashboard / Reports`

No plugin is permitted to bypass the SQLite database or generate an ad-hoc HTML report. The centralized Reporting module consumes `Finding` objects and emits the standardized JSON, HTML, PDF, or Markdown formats.
