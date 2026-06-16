# Production Runbook

## Startup
docker-compose up -d --build

## Shutdown
docker-compose down

## Backup
sqlite3 reconx.db .backup reconx_backup.db

## Restore
Copy backup over volume mount.

## Incident Response
Logs are located at /var/log/reconx/ or via docker logs reconx_api.
