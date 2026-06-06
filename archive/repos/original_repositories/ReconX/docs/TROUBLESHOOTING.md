# ReconX Troubleshooting

## Common Issues

### 1. Database Locked
If using SQLite and you see a "Database is locked" error, ensure no other process (like a DB Browser) is holding a lock on the `projects/<workspace>/reconx.db` file.

### 2. Plugin Timeouts
If a deep scan is failing, increase `timeout_default` in `config.yaml`.

### 3. Missing Output
Ensure you are checking the correct project workspace. Results are saved to `projects/<workspace_name>/outputs/` and the SQLite DB.
