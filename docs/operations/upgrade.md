# ReconX Upgrade Guide

## Upgrading the Docker Container

1. Pull the latest image:
```bash
docker pull reconx:latest
```

2. Stop the current containers:
```bash
docker compose -f deployment/compose/docker-compose.yml down
```

3. Run database migrations:
ReconX applies Alembic migrations on startup, but you can verify them manually if needed via `alembic upgrade head`.

4. Start the updated containers:
```bash
docker compose -f deployment/compose/docker-compose.yml up -d
```

## Rollback Procedure

If the upgrade introduces instability, rollback to the previous version tag:

```bash
# Modify docker-compose.yml to use the specific previous image tag
docker compose -f deployment/compose/docker-compose.yml up -d
```
> Note: If database migrations were applied during the upgrade, you must downgrade the database state before rolling back the application container. Use `alembic downgrade -1`.
