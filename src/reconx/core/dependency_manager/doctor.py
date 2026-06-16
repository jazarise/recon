"""
ReconX Doctor — system health checks for dependencies, config, and environment.
"""
from core.paths import BASE_DIR, WORKFLOWS_DIR, PLUGINS_DIR


import os
import json
import shutil
import sys
from typing import Dict, List



REQUIRED_PYTHON_PACKAGES = [
    "rich", "yaml", "fastapi", "uvicorn", "sqlalchemy",
    "questionary", "requests",
]

OPTIONAL_TOOLS = [
    ("subfinder",  "Subdomain discovery (passive)"),
    ("amass",      "Advanced subdomain enumeration"),
    ("nmap",       "Port scanning and service detection"),
    ("naabu",      "Fast port scanner"),
    ("httpx",      "HTTP probing and fingerprinting"),
    ("katana",     "Fast web crawler"),
    ("hakrawler",  "Web crawler"),
    ("dnsx",       "DNS resolution and enumeration"),
    ("nuclei",     "Vulnerability scanning"),
    ("ffuf",       "Web fuzzer / content discovery"),
    ("gobuster",   "Directory/DNS brute-force"),
    ("feroxbuster","Recursive content discovery"),
    ("gowitness",  "Web screenshot capture"),
    ("gau",        "Historical URL gathering"),
    ("waybackurls","Wayback Machine URL discovery"),
    ("assetfinder","Subdomain discovery"),
    ("findomain",  "Fast subdomain discovery"),
    ("masscan",    "Mass port scanner"),
]

NODEJS_TOOLS = [
    ("node", "Node.js runtime"),
    ("npm", "Node package manager")
]

SYSTEM_BINARIES = [
    ("git", "Version control"),
    ("docker", "Containerization"),
    ("curl", "HTTP client")
]


class Doctor:
    def __init__(self):
        self.checks: List[Dict] = []

    def run_all(self) -> List[Dict]:
        self.checks = []
        self._check_python_version()
        self._check_python_packages()
        self._check_external_tools()
        self._check_nodejs_tools()
        self._check_system_binaries()
        self._check_directories()
        self._check_permissions()
        self._check_workflows()
        self._check_plugins()
        self._check_config()
        self._check_database_write()
        return self.checks
        
    def generate_report(self, path: str = "dependency_report.json"):
        report = {
            "summary": self.summary(),
            "checks": self.checks
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

    # ── individual checks ────────────────────────────────────────────────

    def _check_python_version(self):
        ver = sys.version_info
        ok = ver.major == 3 and ver.minor >= 10
        self._add(
            "Python version",
            ok,
            f"Python {ver.major}.{ver.minor}.{ver.micro}",
            "Python 3.10+ required" if not ok else None,
        )

    def _check_python_packages(self):
        for pkg in REQUIRED_PYTHON_PACKAGES:
            try:
                if pkg == "yaml":
                    import yaml
                elif pkg == "rich":
                    import rich
                elif pkg == "fastapi":
                    import fastapi
                elif pkg == "uvicorn":
                    import uvicorn
                elif pkg == "sqlalchemy":
                    import sqlalchemy
                elif pkg == "questionary":
                    import questionary
                elif pkg == "requests":
                    import requests
                self._add(f"Python package: {pkg}", True, "installed")
            except ImportError:
                self._add(
                    f"Python package: {pkg}", False, "missing",
                    f"Run: pip install {pkg}",
                    is_warning=False,
                )

    def _check_external_tools(self):
        for tool, desc in OPTIONAL_TOOLS:
            path = shutil.which(tool)
            if path:
                self._add(f"Tool: {tool}", True, path, category="tools")
            else:
                self._add(
                    f"Tool: {tool}", None,
                    f"not found — {desc}",
                    f"Install {tool} for enhanced capabilities",
                    is_warning=True,
                    category="tools",
                )

    def _check_nodejs_tools(self):
        for tool, desc in NODEJS_TOOLS:
            path = shutil.which(tool)
            if path:
                self._add(f"NodeJS Tool: {tool}", True, path, category="nodejs")
            else:
                self._add(
                    f"NodeJS Tool: {tool}", None,
                    f"not found — {desc}",
                    f"Install {tool}",
                    is_warning=True,
                    category="nodejs",
                )

    def _check_system_binaries(self):
        for tool, desc in SYSTEM_BINARIES:
            path = shutil.which(tool)
            if path:
                self._add(f"System Binary: {tool}", True, path, category="system")
            else:
                self._add(
                    f"System Binary: {tool}", False,
                    f"not found — {desc}",
                    f"Install {tool}",
                    is_warning=False,
                    category="system",
                )

    def _check_directories(self):
        dirs = {
            "plugins/": PLUGINS_DIR,
            "workflows/": WORKFLOWS_DIR,
            "outputs/": BASE_DIR / "outputs",
            "reports/": BASE_DIR / "reports",
            "logs/": BASE_DIR / "logs",
        }
        for name, path in dirs.items():
            exists = path.exists()
            if not exists:
                path.mkdir(parents=True, exist_ok=True)
            self._add(f"Directory: {name}", True, str(path))

    def _check_permissions(self):
        dirs_to_check = [
            BASE_DIR / "outputs",
            BASE_DIR / "reports",
            BASE_DIR / "logs",
        ]
        for path in dirs_to_check:
            if path.exists():
                writable = os.access(path, os.W_OK)
                self._add(f"Permission (Write): {path.name}", writable, "Writable" if writable else "Not writable")

    def _check_workflows(self):
        for wf in ["basic.yaml", "medium.yaml", "deep.yaml"]:
            path = WORKFLOWS_DIR / wf
            self._add(
                f"Workflow: {wf}",
                path.exists(),
                str(path) if path.exists() else "missing",
                f"Workflow file {wf} is missing" if not path.exists() else None,
            )

    def _check_plugins(self):
        golden = PLUGINS_DIR / "golden"
        for plugin in ["dns_intelligence", "network_discovery", "web_recon", "reporting", "llm_analysis"]:
            adapter = golden / plugin / "adapter.py"
            self._add(
                f"Golden plugin: {plugin}",
                adapter.exists(),
                str(adapter) if adapter.exists() else "missing",
            )

    def _check_config(self):
        cfg_path = BASE_DIR / "config.yaml"
        self._add("Config file: config.yaml", cfg_path.exists(), str(cfg_path))
        env_path = BASE_DIR / ".env"
        self._add(
            "Env file: .env",
            env_path.exists(),
            str(env_path) if env_path.exists() else "not found (optional — needed for API keys)",
            is_warning=True,
        )

    def _check_database_write(self):
        try:
            from core.database import DatabaseManager
            db = DatabaseManager("__doctor_test__")
            sess = db.get_session()
            sess.close()
            db.close()  # Release SQLite file handles before rmtree
            # Clean up
            import shutil as sh
            test_dir = BASE_DIR / "projects" / "__doctor_test__"
            if test_dir.exists():
                sh.rmtree(test_dir, ignore_errors=True)
            self._add("Database write test", True, "SQLite OK")
        except Exception as e:
            self._add("Database write test", False, str(e), "Check SQLite/SQLAlchemy installation")

    # ── helper ──────────────────────────────────────────────────────────
    def _add(
        self,
        name: str,
        status,       # True=pass, False=fail, None=warn
        detail: str = "",
        fix: str = None,
        is_warning: bool = False,
        category: str = "core",
    ):
        if status is False and is_warning:
            status = None
        self.checks.append({
            "name": name,
            "status": status,   # True / False / None(warn)
            "detail": detail,
            "fix": fix,
            "category": category,
        })

    # ── summary ─────────────────────────────────────────────────────────
    def summary(self) -> Dict:
        passed = sum(1 for c in self.checks if c["status"] is True)
        failed = sum(1 for c in self.checks if c["status"] is False)
        warned = sum(1 for c in self.checks if c["status"] is None)
        return {"passed": passed, "failed": failed, "warned": warned, "total": len(self.checks)}
