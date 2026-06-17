# ReconX Disaster Recovery

## Target Metrics
- **RPO (Recovery Point Objective):** 24 hours
- **RTO (Recovery Time Objective):** 4 hours

## Database Restoration

If the primary database fails or becomes corrupted, follow these steps to restore from the latest backup:

1. Stop the `reconx-api` container to prevent new data writes:
```bash
docker stop reconx-api
```

2. Drop and recreate the database:
```bash
docker exec -it reconx-postgres psql -U reconx -c "DROP DATABASE reconx;"
docker exec -it reconx-postgres psql -U reconx -c "CREATE DATABASE reconx;"
```

3. Restore the latest backup:
```bash
gunzip -c /var/backups/reconx/db_backup_latest.sql.gz | docker exec -i reconx-postgres psql -U reconx -d reconx
```

4. Restart the API:
```bash
docker start reconx-api
```
