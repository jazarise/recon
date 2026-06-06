"""
ReconX path configuration — single source of truth for project root.
All modules import PROJECT_ROOT from here instead of hardcoding paths.
"""

from pathlib import Path

# Detect project root dynamically (this file lives in core/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
RESULTS_DIR = PROJECT_ROOT / "results"
LOGS_DIR = PROJECT_ROOT / "logs"
WORKFLOWS_DIR = PROJECT_ROOT / "workflows"
PLUGINS_DIR = PROJECT_ROOT / "plugins"
REPORTS_DIR = PROJECT_ROOT / "reports"
CONFIG_DIR = PROJECT_ROOT / "config"

# Ensure critical directories exist
for d in [OUTPUTS_DIR, RESULTS_DIR, LOGS_DIR, WORKFLOWS_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)
