# ReconX Repository Inventory

**Generated during Stage 0 Stabilization**

This report catalogs the top-level directories remaining in the repository after cleanup.

---

### `src/`
**Purpose**: Core logic, API, engine, core modules, and dashboard frontend.
**File Count**: 10,211 files
**Status**: Active, baseline established. Needs internal structuring review in Stage 1/2.

---

### `tests/`
**Purpose**: Automated testing suites (unit, integration, performance).
**File Count**: 24 files
**Status**: Active. Empty test directories removed. Test discovery should be configured next.

---

### `docs/`
**Purpose**: Project documentation, architectural specs, API documentation, and generated reports.
**File Count**: 2,438 files
**Status**: Active. Includes Stage 0 reports in `docs/reports`.

---

### `plugins/`
**Purpose**: Extensible modules for web, cloud, OSINT, and reporting capabilities.
**File Count**: 7,501 files
**Status**: Active. Restructured to the repository root. Empty plugin templates and directories archived.

---

### `workflows/`
**Purpose**: Defined YAML or Python-based automation workflows and sequences.
**File Count**: 16 files
**Status**: Active. Restructured to the repository root.

---

### `archive/`
**Purpose**: Safe storage for deprecated code, legacy scripts, duplicate modules, and experimental features.
**File Count**: 150 files
**Status**: Managed. Contains `legacy/`, `unused/`, `deprecated/`, `duplicate/`, and `experimental/`.

---

## Conclusion
The repository has been successfully streamlined into 6 primary directories plus core configuration files (like `pyproject.toml`). All redundant folders (`benchmarks`, `examples`, `scripts`, `migrations`) have been archived, and runtime logs/caches have been cleared out.
