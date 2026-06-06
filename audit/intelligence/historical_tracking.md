# Historical Tracking

To answer the question *"What changed since the last scan?"*, ReconX leverages `core/database/models.py`:
- `DBAssetHistory` captures full JSON snapshots of asset profiles.
- `DBFindingHistory` flags when a specific finding transitions between `new`, `open`, `remediated`, or `accepted`.
- `DBScanHistory` tracks metric execution bounds.
