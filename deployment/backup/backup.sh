#!/bin/bash
set -e

BACKUP_DIR="/var/backups/reconx"
DB_CONTAINER="reconx-postgres"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "Starting database backup..."
docker exec -t $DB_CONTAINER pg_dumpall -c -U reconx > "$BACKUP_DIR/db_backup_$DATE.sql"

echo "Compressing backup..."
gzip "$BACKUP_DIR/db_backup_$DATE.sql"

echo "Cleaning up old backups (keeping last 7 days)..."
find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +7 -exec rm {} \;

echo "Backup complete: db_backup_$DATE.sql.gz"
