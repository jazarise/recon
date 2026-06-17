# ReconX Maintainers

This document lists the individuals responsible for the long-term governance and maintenance of the ReconX platform.

## Core Maintainers
The Core Maintainers have push access to the `main` branch and have final say in architectural decisions.

- **@reconx/backend-lead**: Focuses on FastAPI, SQLAlchemy, and API endpoints.
- **@reconx/security-lead**: Focuses on RBAC, JWT, and Sandbox security.
- **@reconx/workflow-lead**: Focuses on the DAG engine and task scheduling.

## Reviewers
Reviewers can approve Pull Requests, but cannot merge them directly into `main`.

- **@reconx/plugin-reviewers**: Responsible for validating third-party plugins against our security SDK.

## Release Managers
- **@reconx/devops**: Responsible for cutting tags, building Docker images, and managing the CI/CD pipeline.

## Security Contacts
To report a vulnerability privately, please contact the security team directly. Do **not** open a public issue. See `SECURITY.md` for details.
