# ReconX User Guide

Welcome to the comprehensive user guide for ReconX. This guide covers all the core concepts and operational workflows required to use the platform effectively.

## Core Concepts

### Projects
A **Project** is the highest level of organization in ReconX. Think of it as an engagement or a specific assessment.
- **Purpose**: Grouping related targets, workflows, and findings to isolate different assessments.
- **Usage**: `reconx project create <NAME>`

### Targets
A **Target** defines the initial scope (e.g., domain names, IP addresses) associated with a project.
- **Purpose**: Providing seed data for workflows to start enumerating.
- **Usage**: `reconx target add <PROJECT_ID> <TARGET_STRING>`

### Assets
An **Asset** is any discovered infrastructure (subdomains, open ports, web applications).
- **Purpose**: The result of reconnaissance workflows. ReconX normalizes and deduplicates assets.
- **Usage**: `reconx assets list --project-id <PROJECT_ID>`

### Findings
A **Finding** is a vulnerability or security risk discovered on an asset.
- **Purpose**: Tracking actionable security issues.
- **Usage**: `reconx findings list --project-id <PROJECT_ID>`

### Reports & Dashboards
ReconX can aggregate findings and assets into shareable formats (JSON, CSV, PDF).
- **Purpose**: Communicating risk to stakeholders.
- **Usage**: `reconx reports generate --project-id <PROJECT_ID> --format pdf`

## Advanced Operations

### Workflows
A **Workflow** is a YAML file defining a directed acyclic graph (DAG) of plugin executions.
- **Purpose**: Automating sequential security tooling without manual intervention.
- **Usage**: `reconx workflow run <WORKFLOW_NAME> <TARGET>`

### Plugins
A **Plugin** is a wrapper around a specific security tool (e.g., `subfinder`, `nmap`).
- **Purpose**: Executing a tool and translating its output into the standard ReconX Asset/Finding schema.
- **Usage**: `reconx plugins list`

## Troubleshooting
- **No assets found**: Ensure your target string is valid and that the plugins in your workflow are correctly installed on the host running the worker.
- **Authentication errors**: Verify that your `jwt_secret` matches across API server instances and you are passing a valid `Authorization: Bearer <TOKEN>` header.
