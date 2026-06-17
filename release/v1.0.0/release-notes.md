# ReconX v1.0.0 Release Notes

Welcome to the official v1.0.0 release of ReconX!

## Features
- **Authentication**: JWT-based access tokens and secure refresh mechanisms.
- **Plugins**: A robust SDK abstracting underlying CLI tools safely.
- **Workflows**: A Directed Acyclic Graph (DAG) engine for orchestrating sequential and parallel reconnaissance tasks.
- **Intelligence**: An automated asset normalizer, correlator, and deduplicator that builds a queryable attack surface graph.
- **Reporting**: Export your findings and assets to PDF, JSON, HTML, or CSV.

## Security
- **RBAC**: Strict Viewer, Operator, and Admin roles applied via FastAPI dependencies.
- **Audit Logs**: All sensitive actions are logged.
- **Plugin Validation**: Strict input sanitization preventing command injection.

## Infrastructure
- **CI/CD**: Fully automated testing, linting, and security scanning.
- **Monitoring**: Prometheus metrics (`/metrics`) and Kubernetes-ready health checks.
- **Docker**: Multi-stage, non-root container images for production deployment.
