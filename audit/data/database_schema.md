# Database Schema

ReconX uses SQLAlchemy for ORM mapping to SQLite (or PostgreSQL).

Tables:
- `targets` (DBTarget)
- `hosts` (DBHost)
- `subdomains` (DBSubdomain)
- `ports` (DBPort)
- `services` (DBService)
- `technologies` (DBTechnology)
- `vulnerabilities` (DBVulnerability)
- `findings` (DBFinding) - Central unified storage.
- `scans` (DBScan)
