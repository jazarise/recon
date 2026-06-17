# ReconX Backup Procedures

## Database Backup
The ReconX database (PostgreSQL) should be backed up regularly to prevent data loss.
A daily incremental and weekly full backup strategy is recommended.

### Manual Backup
To manually trigger a backup using the provided script:
```bash
bash deployment/backup/backup.sh
```

This script will:
- Dump the `reconx-postgres` container database to an SQL file.
- Compress the dump using `gzip`.
- Retain backups for the last 7 days and delete older files to save disk space.

## Reports & Configuration Backup
In addition to the database, configuration files (e.g. `config/*.yaml`) and generated `reports/` should also be backed up.
```bash
tar -czvf reconx_assets_backup_$(date +%F).tar.gz config/ reports/
```
