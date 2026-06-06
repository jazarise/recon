# Correlation Engine Design

The Correlation Engine translates flat `DBFinding` rows into highly connected context networks.
- Uses `core/correlation/rules.py` to identify duplicates across scans and collapse them.
- Uses `core/correlation/relationships.py` to assert edge links (e.g. Domain `resolves_to` IP, IP `exposes` Port, Port `affected_by` Vulnerability).
