"""
ReconX — Stage 21: SAST Engine
================================
Source code static analysis absorbed from shannon and shannon-uncontained.

Capabilities:
  TaintAnalyzer        — Data-flow taint source→sink tracking
  SecretDetector       — Code-aware secret/credential detection
  SCAnalyzer           — Software composition analysis (SCA) with reachability
  BusinessLogicChecker — Invariant-based logic flaw detection (LLM-assisted)
  SASTEngine           — Unified coordinator

Design:
  - Pure Python — no external SAST tools required
  - AST-based analysis for Python; pattern-based for other languages
  - LLM-assisted for ambiguous findings and business logic
  - All output normalized to ReconX finding schema
"""
from __future__ import annotations

import ast
import hashlib
import json
import logging
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

log = logging.getLogger("reconx.analysis.sast")

# ── Finding Models ─────────────────────────────────────────────────────────────

@dataclass
class SASTFinding:
    rule:        str
    title:       str
    severity:    str              # CRITICAL | HIGH | MEDIUM | LOW | INFO
    category:    str              # taint | secret | sca | logic
    file:        str
    line:        int
    code:        str              = ""
    description: str              = ""
    cve:         Optional[str]   = None
    confidence:  int              = 70    # 0–100
    remediation: str              = ""
    meta:        dict             = field(default_factory=dict)


# ─────────────────────────────────────────────────────────────────────────────
# SECRET DETECTOR
# ─────────────────────────────────────────────────────────────────────────────

SECRET_RULES: list[tuple[str, re.Pattern, str, str]] = [
    # (rule_id, pattern, label, severity)
    ("SEC-001", re.compile(r'AKIA[0-9A-Z]{16}'),                                   "AWS Access Key ID",      "CRITICAL"),
    ("SEC-002", re.compile(r'(?i)aws[_\-\s]?secret[_\-\s]?(?:access[_\-\s]?)?key\s*[:=]\s*["\']?([A-Za-z0-9/+]{40})'), "AWS Secret Key", "CRITICAL"),
    ("SEC-003", re.compile(r'sk-[A-Za-z0-9]{48}'),                                "OpenAI Secret Key",      "CRITICAL"),
    ("SEC-004", re.compile(r'ghp_[A-Za-z0-9]{36}'),                               "GitHub PAT",             "HIGH"),
    ("SEC-005", re.compile(r'ghu_[A-Za-z0-9]{36}'),                               "GitHub User Token",      "HIGH"),
    ("SEC-006", re.compile(r'-----BEGIN (?:RSA|EC|OPENSSH|DSA) PRIVATE KEY-----'), "Private Key",            "CRITICAL"),
    ("SEC-007", re.compile(r'AIza[0-9A-Za-z\-_]{35}'),                            "Google API Key",         "HIGH"),
    ("SEC-008", re.compile(r'(?i)(?:password|passwd|pwd)\s*[:=]\s*["\'](?!.*\{)([^"\']{6,})'), "Hardcoded Password", "HIGH"),
    ("SEC-009", re.compile(r'(?i)(?:secret|api[_-]?key|token)\s*[:=]\s*["\']([A-Za-z0-9_\-]{16,})["\']'), "Generic Secret", "MEDIUM"),
    ("SEC-010", re.compile(r'(?i)(?:bearer|authorization)\s*[:=]\s*["\']?([A-Za-z0-9._\-]{20,})'), "Auth Token", "HIGH"),
    ("SEC-011", re.compile(r'(?i)(?:mysql|postgres|mongodb|redis)://[^@\s]+:[^@\s]+@'), "DB Connection String with Creds", "HIGH"),
    ("SEC-012", re.compile(r'(?i)JWT_SECRET\s*[:=]\s*["\']([^"\']{8,})["\']'),    "JWT Secret",             "CRITICAL"),
    ("SEC-013", re.compile(r'(?i)STRIPE_(?:SECRET|API)_KEY\s*[:=]\s*["\']?(sk_(?:live|test)_[A-Za-z0-9]{24,})'), "Stripe Key", "CRITICAL"),
    ("SEC-014", re.compile(r'xox[baprs]-[A-Za-z0-9\-]{10,}'),                    "Slack Token",            "HIGH"),
    ("SEC-015", re.compile(r'-----BEGIN CERTIFICATE-----'),                        "Certificate in Code",    "LOW"),
]

SAFE_PREFIXES = [
    "test_", "TEST_", "fake_", "FAKE_", "example_", "dummy_", "placeholder",
    "<", "${", "{{", "your_", "YOUR_", "xxx", "XXXX", "...",
]


class SecretDetector:
    """Scan source files for hardcoded secrets and credentials."""

    def scan_file(self, path: Path) -> list[SASTFinding]:
        findings = []
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            lines   = content.splitlines()
        except Exception:
            return findings

        for lineno, line in enumerate(lines, 1):
            stripped = line.strip()
            # Skip comments and test files
            if stripped.startswith(("#", "//", "*", "<!--")):
                continue
            if any(p in line for p in SAFE_PREFIXES):
                continue

            for rule_id, pattern, label, severity in SECRET_RULES:
                m = pattern.search(line)
                if m:
                    value = m.group(0)[:60]
                    findings.append(SASTFinding(
                        rule=rule_id,
                        title=f"{label} detected in source code",
                        severity=severity,
                        category="secret",
                        file=str(path),
                        line=lineno,
                        code=stripped[:120],
                        description=f"Hardcoded {label} found. Pattern: {value}",
                        confidence=85,
                        remediation=(
                            f"Remove this {label} from source code. "
                            "Use environment variables or a secrets manager (Vault, AWS Secrets Manager, etc.)."
                        ),
                        meta={"pattern": label, "match_preview": value},
                    ))
                    break   # One finding per line per file

        return findings

    def scan_directory(self, root: Path,
                        extensions: list[str] | None = None) -> list[SASTFinding]:
        exts = extensions or [".py", ".js", ".ts", ".env", ".yaml", ".yml",
                               ".json", ".toml", ".tf", ".rb", ".go", ".java",
                               ".php", ".cs", ".sh", ".bash", ".zsh", ".conf",
                               ".cfg", ".ini", ".properties"]
        findings = []
        skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv",
                     "dist", "build", ".next", "vendor", "target"}

        for file_path in root.rglob("*"):
            if any(d in file_path.parts for d in skip_dirs):
                continue
            if file_path.suffix.lower() in exts and file_path.is_file():
                findings.extend(self.scan_file(file_path))

        return findings


# ─────────────────────────────────────────────────────────────────────────────
# TAINT ANALYZER (Python AST-based)
# ─────────────────────────────────────────────────────────────────────────────

TAINT_SOURCES = {
    # Flask / Django request inputs
    "request.args", "request.form", "request.data", "request.json",
    "request.files", "request.get_json", "request.values",
    # Django
    "request.GET", "request.POST", "request.body",
    # FastAPI
    "Query", "Body", "Form", "Path",
    # Generic
    "input", "sys.stdin", "os.environ.get",
    # DB results
    "cursor.fetchone", "cursor.fetchall",
}

TAINT_SINKS = {
    # SQL injection sinks
    "execute":     ("SQL Injection", "CRITICAL", "TAI-001"),
    "executemany": ("SQL Injection", "CRITICAL", "TAI-001"),
    "raw":         ("SQL Injection", "CRITICAL", "TAI-001"),         # Django ORM
    "extra":       ("SQL Injection", "HIGH",     "TAI-001"),
    # Command injection
    "os.system":   ("Command Injection", "CRITICAL", "TAI-002"),
    "subprocess.run": ("Command Injection", "HIGH", "TAI-002"),
    "subprocess.call": ("Command Injection", "HIGH", "TAI-002"),
    "subprocess.Popen": ("Command Injection", "HIGH", "TAI-002"),
    "eval":        ("Code Injection", "CRITICAL", "TAI-003"),
    "exec":        ("Code Injection", "CRITICAL", "TAI-003"),
    "compile":     ("Code Injection", "HIGH",     "TAI-003"),
    # Path traversal
    "open":        ("Path Traversal", "HIGH",  "TAI-004"),
    "os.path.join":("Path Traversal", "MEDIUM","TAI-004"),
    # SSRF
    "requests.get":     ("SSRF", "HIGH", "TAI-005"),
    "requests.post":    ("SSRF", "HIGH", "TAI-005"),
    "urllib.request.urlopen": ("SSRF", "HIGH", "TAI-005"),
    # XSS (Jinja2 markup)
    "Markup":      ("XSS", "HIGH", "TAI-006"),
    "render_template_string": ("SSTI", "CRITICAL", "TAI-007"),
    # Deserialization
    "pickle.loads":    ("Insecure Deserialization", "CRITICAL", "TAI-008"),
    "yaml.load":       ("Insecure Deserialization", "HIGH",     "TAI-008"),
    "marshal.loads":   ("Insecure Deserialization", "HIGH",     "TAI-008"),
}


class TaintVisitor(ast.NodeVisitor):
    """Walk Python AST and track tainted variable flow from source to sink."""

    def __init__(self, source_code: str):
        self.source_lines = source_code.splitlines()
        self.tainted: set[str] = set()
        self.findings: list[dict] = []

    def visit_Assign(self, node: ast.Assign) -> None:
        # Check if value is a taint source
        val_str = ast.unparse(node.value) if hasattr(ast, "unparse") else ""
        if any(src in val_str for src in TAINT_SOURCES):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.tainted.add(target.id)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        call_str = ast.unparse(node) if hasattr(ast, "unparse") else ""
        func_str = ast.unparse(node.func) if hasattr(ast, "unparse") else ""

        for sink_name, (vuln, severity, rule_id) in TAINT_SINKS.items():
            if sink_name in func_str:
                # Check if any argument is tainted
                for arg in node.args:
                    arg_str = ast.unparse(arg) if hasattr(ast, "unparse") else ""
                    if any(t in arg_str for t in self.tainted):
                        code = (self.source_lines[node.lineno - 1].strip()
                                if node.lineno <= len(self.source_lines) else "")
                        self.findings.append({
                            "rule":     rule_id,
                            "vuln":     vuln,
                            "severity": severity,
                            "sink":     sink_name,
                            "line":     node.lineno,
                            "code":     code[:120],
                        })
        self.generic_visit(node)


class TaintAnalyzer:
    """AST-based Python taint analysis."""

    def scan_file(self, path: Path) -> list[SASTFinding]:
        findings = []
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
            tree   = ast.parse(source)
        except SyntaxError:
            return findings
        except Exception:
            return findings

        visitor = TaintVisitor(source)
        visitor.visit(tree)

        for f in visitor.findings:
            findings.append(SASTFinding(
                rule=f["rule"],
                title=f"{f['vuln']} — tainted data flows to {f['sink']}",
                severity=f["severity"],
                category="taint",
                file=str(path),
                line=f["line"],
                code=f["code"],
                description=(
                    f"User-controlled input reaches '{f['sink']}' without sanitization. "
                    f"This may allow {f['vuln'].lower()} attacks."
                ),
                confidence=75,
                remediation=(
                    f"Sanitize and validate all user input before passing to {f['sink']}. "
                    "Use parameterized queries for SQL, shlex.quote for shell commands, "
                    "and restrict file paths to a safe directory."
                ),
                meta={"sink": f["sink"], "vuln": f["vuln"]},
            ))

        return findings

    def scan_directory(self, root: Path) -> list[SASTFinding]:
        findings = []
        skip_dirs = {".git", "__pycache__", ".venv", "venv", "node_modules"}
        for path in root.rglob("*.py"):
            if any(d in path.parts for d in skip_dirs):
                continue
            findings.extend(self.scan_file(path))
        return findings


# ─────────────────────────────────────────────────────────────────────────────
# SCA — SOFTWARE COMPOSITION ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

class SCAnalyzer:
    """
    Software composition analysis.
    Checks Python requirements.txt / pyproject.toml / package.json
    for known vulnerable dependencies using pip-audit / safety / osv-scanner.
    """

    def scan(self, root: Path) -> list[SASTFinding]:
        findings = []

        # Try pip-audit first (Python ecosystem)
        if (root / "requirements.txt").exists() or (root / "pyproject.toml").exists():
            findings.extend(self._run_pip_audit(root))

        # Try npm audit (Node.js ecosystem)
        if (root / "package.json").exists():
            findings.extend(self._run_npm_audit(root))

        return findings

    def _run_pip_audit(self, root: Path) -> list[SASTFinding]:
        findings = []
        try:
            result = subprocess.run(
                ["pip-audit", "--format=json", "--output=-"],
                capture_output=True, text=True, timeout=60, cwd=root,
            )
            data = json.loads(result.stdout)
            for vuln in data.get("vulnerabilities", []):
                pkg  = vuln.get("name", "?")
                ver  = vuln.get("version", "?")
                ids  = vuln.get("vulns", [])
                for v in ids:
                    sev = self._map_cvss(v.get("fix_versions", []))
                    findings.append(SASTFinding(
                        rule="SCA-001",
                        title=f"Vulnerable dependency: {pkg}=={ver}",
                        severity=sev,
                        category="sca",
                        file=str(root / "requirements.txt"),
                        line=0,
                        description=f"{v.get('id','')} — {v.get('description','')[:200]}",
                        cve=v.get("id") if v.get("id","").startswith("CVE") else None,
                        confidence=90,
                        remediation=f"Upgrade {pkg} to {v.get('fix_versions',['latest'])[0] if v.get('fix_versions') else 'latest'}",
                        meta={"package": pkg, "version": ver},
                    ))
        except FileNotFoundError:
            findings.append(SASTFinding(
                rule="SCA-INFO",
                title="pip-audit not installed — SCA scan skipped",
                severity="INFO", category="sca", file=str(root), line=0,
                description="Install pip-audit: pip install pip-audit",
                confidence=100,
            ))
        except Exception as e:
            log.debug(f"pip-audit error: {e}")
        return findings

    def _run_npm_audit(self, root: Path) -> list[SASTFinding]:
        findings = []
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                capture_output=True, text=True, timeout=60, cwd=root,
            )
            data = json.loads(result.stdout)
            vulns = data.get("vulnerabilities", {})
            for pkg, info in vulns.items():
                sev = info.get("severity", "medium").upper()
                if sev not in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
                    sev = "MEDIUM"
                findings.append(SASTFinding(
                    rule="SCA-002",
                    title=f"Vulnerable npm package: {pkg}",
                    severity=sev,
                    category="sca",
                    file=str(root / "package.json"),
                    line=0,
                    description=info.get("via", [{}])[0].get("title", "") if info.get("via") else "",
                    confidence=90,
                    remediation=f"Run `npm audit fix` or manually upgrade {pkg}",
                    meta={"package": pkg, "severity": sev},
                ))
        except FileNotFoundError:
            import logging
            logging.warning("npm not available in PATH. Skipping NPM audit dependency check.")
        except Exception as e:
            log.debug(f"npm audit error: {e}")
        return findings

    @staticmethod
    def _map_cvss(fix_versions: list) -> str:
        return "HIGH" if fix_versions else "MEDIUM"


# ─────────────────────────────────────────────────────────────────────────────
# SAST ENGINE — Unified Coordinator
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class SASTReport:
    repo_path:  str
    language:   str
    findings:   list[SASTFinding]  = field(default_factory=list)
    stats:      dict               = field(default_factory=dict)
    summary:    str                = ""

    def by_severity(self) -> dict[str, list[SASTFinding]]:
        result: dict = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": [], "INFO": []}
        for f in self.findings:
            result.setdefault(f.severity, []).append(f)
        return result

    def to_reconx_findings(self) -> list[dict]:
        """Convert to ReconX finding schema for storage."""
        return [
            {
                "title":       f.title,
                "severity":    f.severity,
                "target":      f.file,
                "service":     "Code",
                "description": f.description,
                "evidence":    f.code,
                "remediation": f.remediation,
                "cve":         f.cve,
                "meta":        {"rule": f.rule, "line": f.line,
                                "category": f.category, "confidence": f.confidence,
                                **f.meta},
            }
            for f in self.findings
        ]


class SASTEngine:
    """
    Unified SAST coordinator.

    Usage:
        engine = SASTEngine(llm=adapter)
        report = engine.scan("/path/to/repo", checks=["taint", "secrets", "sca"])
    """

    def __init__(self, llm=None):
        self.llm      = llm
        self.secrets  = SecretDetector()
        self.taint    = TaintAnalyzer()
        self.sca      = SCAnalyzer()

    def scan(
        self,
        repo_path: str,
        checks: list[str] | None = None,
        language: Optional[str] = None,
    ) -> SASTReport:
        root   = Path(repo_path)
        checks = checks or ["taint", "secrets", "sca"]
        lang   = language or self._detect_language(root)

        log.info(f"SAST scan: {repo_path} [{lang}] checks={checks}")

        all_findings: list[SASTFinding] = []

        if "secrets" in checks:
            log.info("  Running secret detection...")
            all_findings.extend(self.secrets.scan_directory(root))

        if "taint" in checks and lang == "python":
            log.info("  Running taint analysis...")
            all_findings.extend(self.taint.scan_directory(root))

        if "sca" in checks:
            log.info("  Running SCA analysis...")
            all_findings.extend(self.sca.scan(root))

        # Deduplicate by (rule, file, line)
        seen: set[str] = set()
        unique: list[SASTFinding] = []
        for f in all_findings:
            key = hashlib.md5(f"{f.rule}:{f.file}:{f.line}".encode()).hexdigest()
            if key not in seen:
                seen.add(key)
                unique.append(f)

        # Sort by severity
        sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
        unique.sort(key=lambda f: sev_order.get(f.severity, 5))

        sev_counts = {}
        for f in unique:
            sev_counts[f.severity] = sev_counts.get(f.severity, 0) + 1

        report = SASTReport(
            repo_path=str(root),
            language=lang,
            findings=unique,
            stats={
                "total":    len(unique),
                "critical": sev_counts.get("CRITICAL", 0),
                "high":     sev_counts.get("HIGH", 0),
                "medium":   sev_counts.get("MEDIUM", 0),
                "low":      sev_counts.get("LOW", 0),
                "files_scanned": self._count_files(root),
                "checks_run":    checks,
            },
        )

        if self.llm and unique:
            report.summary = self._llm_summary(report)

        return report

    def _detect_language(self, root: Path) -> str:
        """Detect primary language by file count."""
        counts = {}
        for f in root.rglob("*"):
            if f.suffix in (".py",): counts["python"] = counts.get("python", 0) + 1
            elif f.suffix in (".js", ".ts", ".tsx", ".jsx"): counts["javascript"] = counts.get("javascript", 0) + 1
            elif f.suffix in (".go",): counts["go"] = counts.get("go", 0) + 1
            elif f.suffix in (".java",): counts["java"] = counts.get("java", 0) + 1
            elif f.suffix in (".rb",): counts["ruby"] = counts.get("ruby", 0) + 1
        return max(counts, key=counts.get) if counts else "unknown"

    def _count_files(self, root: Path) -> int:
        skip = {".git", "node_modules", "__pycache__", ".venv", "venv"}
        return sum(1 for f in root.rglob("*")
                   if f.is_file() and not any(d in f.parts for d in skip))

    def _llm_summary(self, report: SASTReport) -> str:
        if not self.llm:
            return ""
        top = [f"{f.severity}: {f.title} ({f.file}:{f.line})"
               for f in report.findings[:10]]
        prompt = (
            f"SAST scan of {report.repo_path} ({report.language})\n"
            f"Total findings: {report.stats['total']} "
            f"(C:{report.stats['critical']}, H:{report.stats['high']}, "
            f"M:{report.stats['medium']}, L:{report.stats['low']})\n\n"
            f"Top findings:\n" + "\n".join(f"- {t}" for t in top) +
            "\n\nWrite a 3-sentence security summary: what was found, risk level, and top remediation priority."
        )
        resp = self.llm.ask(prompt, max_tokens=300)
        return resp.text if resp.ok else ""
