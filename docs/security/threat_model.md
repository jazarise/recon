# ReconX Threat Model

This document outlines the high-level security architecture, threat landscape, and mitigation strategies for the ReconX platform.

## Assets
- **Vulnerability Data:** Discovered findings mapping to client infrastructure.
- **API Keys / Secrets:** Credentials utilized by ReconX plugins to access premium OSINT feeds (e.g. Shodan).
- **Execution Environment:** The host server operating the ReconX Orchestrator.

## Trust Boundaries
- **External Web Traffic <-> API Layer:** Untrusted traffic interacting with the REST API.
- **Plugins <-> Execution Environment:** Third-party OS binaries invoked by plugins interacting with the local filesystem.
- **Admin <-> Configuration:** The environment variable `.env` file containing secrets.

## Attack Surfaces
- **REST API Endpoints:** Susceptible to parameter tampering, authentication bypass.
- **Workflow YAMLs:** Parsing logic susceptible to unsafe deserialization.
- **Subprocess Wrappers:** Plugin execution invoking `shell=True` commands susceptible to shell injection via poisoned target arguments.
- **Export Writers:** File persistence vulnerable to path traversal.

## Threats (STRIDE)
- **Spoofing:** Bypassing API authentication to trigger rogue scans.
- **Tampering:** Modifying `.yaml` workflows or DB contents via SQL injection.
- **Repudiation:** Deleting scan traces (mitigated by enforced logging).
- **Information Disclosure:** Leaking API keys or verbose Python stack traces on 500 errors.
- **Denial of Service:** Overloading the `TaskQueue` without rate limiting.
- **Elevation of Privilege:** Shell injection escalating out of the ReconX python process into root OS control.

## Mitigations
- Shell execution is strictly parameterized as arrays (`shell=False`).
- Workflows parse via `yaml.safe_load`.
- Configuration secrets are decoupled into environment variables via Pydantic `Settings`.
- Dependencies enforce JWT authentication and rate-limiting.

## Residual Risk
- As an offensive orchestration tool, ReconX relies on third-party security binaries (nuclei, nmap). A zero-day vulnerability in these underlying external tools could still compromise the container environment.
