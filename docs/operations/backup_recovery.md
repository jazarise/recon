# Backup & Recovery Procedures

## Configuration Backup
Back up `.env` and `config/*.yaml`.

## Database Backup
`sqlite3 data/reconx.db ".backup 'reconx_backup.db'"`

## Restore
Mount the backup SQLite file into the container volume and restart `docker-compose`.
