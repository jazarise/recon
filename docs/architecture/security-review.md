# Security Review (v1.0.0)

A comprehensive security review of the ReconX platform was conducted for the v1.0 release.

## Subsystem Posture

### Authentication
- Uses `passlib[bcrypt]` for password hashing.
- JWT tokens are signed using HS256. The `JWT_SECRET_KEY` is enforced as a required environment variable (no fallback defaults in production).

### Authorization
- Enforced via FastAPI dependencies (`get_current_active_user`, `require_role`).
- Tested extensively for horizontal and vertical privilege escalation. No bypasses found.

### Input Validation
- **API**: Handled strictly by Pydantic v2 schemas. Unknown fields are stripped.
- **CLI/Plugins**: Targets are validated via `sdk.plugin_sdk.validators.validate_target` using regex to prevent command injection.

### Plugin Execution
- **OS Command Injection**: `shell=True` is prohibited globally across the SDK and core. Commands are passed as lists to `asyncio.create_subprocess_exec`.
- **Blast Radius**: Docker containers run as a non-root user.

### Reporting Security
- Server-Side XSS via malicious asset names is mitigated by Jinja2's default auto-escaping feature.

### Secrets Management
- All database credentials, JWT secrets, and third-party API keys are loaded via environment variables (`.env`). No secrets are hardcoded in the repository.

## Automated Scanning
- `bandit -r src`: Passed (0 High severity issues).
- `pip-audit`: Verified against known CVEs in upstream dependencies.
