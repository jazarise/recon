# Dead Code & Artifacts Report

This report catalogs dead code, empty directories, and duplicate files identified during Stage 0 of the ReconX stabilization process.

All items listed below have been successfully moved to the `archive/unused/` directory to declutter the repository while preserving history.

## Empty Python Files (`__init__.py`)

- `docs/__init__.py`
- `plugins/dns/__init__.py`
- `plugins/experimental/__init__.py`
- `plugins/experimental/discovery/__init__.py`
- `plugins/experimental/vuln/scanning/__init__.py`
- `plugins/experimental/vuln/vulnerabilities/__init__.py`
- `plugins/osint/__init__.py`
- `plugins/reporting/__init__.py`
- `plugins/web/__init__.py`
- `src/reconx/__init__.py`
- `src/reconx/agents/__init__.py`
- `src/reconx/api/__init__.py`
- `src/reconx/core/ai/__init__.py`
- `src/reconx/core/analytics/__init__.py`
- `src/reconx/core/api/__init__.py`
- `src/reconx/core/auth/__init__.py`
- `src/reconx/core/dashboard/__init__.py`
- `src/reconx/core/dependency_manager/__init__.py`
- `src/reconx/core/engine/__init__.py`
- `src/reconx/core/logging/__init__.py`
- `src/reconx/core/operations/__init__.py`
- `src/reconx/core/plugin_manager/__init__.py`
- `src/reconx/database/__init__.py`
- `src/reconx/modules/__init__.py`
- `src/reconx/modules/api/__init__.py`
- `src/reconx/modules/cloud/__init__.py`
- `src/reconx/modules/osint/__init__.py`
- `src/reconx/modules/reporting/__init__.py`
- `src/reconx/modules/web/__init__.py`
- `src/reconx/sdk/__init__.py`
- `workflows/__init__.py`

## Empty Directories

- `plugins/active`
- `plugins/integrations`
- `plugins/passive`
- `plugins/osint/deep/active_recon`
- `plugins/osint/deep/asn_intel`
- `plugins/osint/deep/content_discovery`
- `plugins/osint/deep/csp_extractor`
- `plugins/osint/deep/graphql_scan`
- `plugins/osint/deep/httpx`
- `plugins/osint/deep/naabu`
- `plugins/osint/deep/nuclei`
- `plugins/osint/deep/passive_recon`
- `plugins/osint/deep/subfinder`
- `plugins/osint/deep/xss_scan`
- `plugins/reporting/golden/malicious`
- `src/reconx/config`
- `src/reconx/sdk`
- `src/reconx/core/engine`
- `src/reconx/core/logging`
- `src/reconx/dashboard/frontend/node_modules/.vite-temp`
- `tests/dashboard`
- `tests/performance`

## Duplicate/Unreferenced

*During scanning, no specific large-scale duplicate Python logic outside of archived legacy components was identified. Duplicate components from earlier stages have been safely moved to `archive/legacy` and `archive/unused`.*
