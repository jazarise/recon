# Database Layer Audit

The ReconX Database Layer contains the SQLAlchemy schema mappings representing the application's persistent state.

## Findings

*   The primary database definitions are securely localized to `src/reconx/database/schema/models.py`.
*   **Duplicate Database Root:** An entire duplicate database interface, including its own schema models and ORM sessions, was present under `src/reconx/core/reconx/db`. This was eliminated during the nested core duplication purge.
*   **Schema Review:** `models.py` defines standard ORM definitions (e.g. Scans, Assets, Reports). No orphan or unmapped tables exist natively in the primary model file.

## Resolution

The application relies entirely on `reconx.database.schema.models` for its data constraints. No duplicate schemas exist.
