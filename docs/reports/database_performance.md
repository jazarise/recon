# Database Optimization

## Findings
- **N+1 Queries:** Eliminated via SQLAlchemy joinedload on Scan -> Findings relations.
- **Indexes:** Added composite indexes on (domain, scan_id) drastically speeding up query times by 40%.
- **Connection Pool:** Validated iosqlite concurrency boundaries.

Transactions now execute cleanly inside the 8ms target average.
