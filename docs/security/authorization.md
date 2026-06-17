# Authorization (RBAC)

ReconX implements **Role-Based Access Control (RBAC)** to restrict platform capabilities.

## Roles

- **Viewer**: Read-only access. Can view projects, assets, and reports. Cannot run workflows.
- **Operator**: Read-write access. Can create targets, run workflows, and manage findings.
- **Admin**: Full platform access. Can manage users, alter global configuration, and access audit logs.

## Enforcement
Roles are enforced using FastAPI dependency injection (`get_current_active_user`, `require_role`). If an unauthorized user attempts to hit an endpoint, the API immediately returns `403 Forbidden`.
