"""
ReconX path configuration — single source of truth for project root.
All modules import BASE_DIR from here instead of hardcoding paths.
"""

from pathlib import Path

# Detect project root dynamically (this file lives in core/)
BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUTS_DIR = BASE_DIR / "outputs"
RESULTS_DIR = BASE_DIR / "results"
LOGS_DIR = BASE_DIR / "logs"
WORKFLOWS_DIR = BASE_DIR / "workflows"
PLUGINS_DIR = BASE_DIR / "plugins"
REPORTS_DIR = BASE_DIR / "reports"
CONFIG_DIR = BASE_DIR / "config"

# Ensure critical directories exist
for d in [OUTPUTS_DIR, RESULTS_DIR, LOGS_DIR, WORKFLOWS_DIR, REPORTS_DIR, PLUGINS_DIR, CONFIG_DIR]:
    try:
        d.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
