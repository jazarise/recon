# Plugin Security

Executing third-party code (or binaries) carries inherent risk.

## Sandboxing
Plugins are executed via a strict `subprocess` wrapper. 
- `shell=True` is **strictly prohibited**. All commands must be executed as an array of arguments to prevent command injection.
- Containerized deployments run the API as a non-root `reconx` user, restricting file system access and limiting the blast radius of a compromised tool.

## Input Validation
All targets passed to plugins are validated against Pydantic models. We sanitize IP addresses, domains, and URLs before they ever reach the underlying CLI tool.
