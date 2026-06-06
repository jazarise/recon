# Security Design

- **Authentication:** JWT-based stateless authentication (`/api/auth/login`).
- **RBAC:** `DBUser` table incorporates `role` definitions (Admin, Operator, ReadOnly).
- **Session Protection:** API endpoints will require bearer tokens.
- **Raw Execution Defense:** The Dashboard cannot execute raw shell commands, it only triggers validated YAML Workflows.
