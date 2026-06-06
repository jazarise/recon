# Upgrade & Backward Compatibility Policy

ReconX enforces a strict upgrade policy to protect operator data.

1. **Database:** Migrations are handled exclusively via `alembic upgrade head`. Never manually drop tables.
2. **API Endpoints:** V1 endpoints will be prefixed with `/api/v1/`. They are supported for 1 full Major release before deprecation.
3. **Plugin Interfaces:** `sdk/plugin_base.py` is guaranteed stable through v2.x. Breaking changes will only occur in v3.0.
