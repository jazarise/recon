"""Stage 1 capability mapper for ReconX.

Reads the immutable source pools (pccc and allfiles) and writes the required
classification artifacts under intelligence/. The script intentionally does not
modify either source root.
"""

from __future__ import annotations

import ast
import collections
import hashlib
import json
import re
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parents[1]
SOURCE_ROOTS = [BASE / "pccc", BASE / "allfiles"]
OUT = BASE / "intelligence"

REQUIRED_CATEGORIES = [
    "Recon",
    "Web Scanning",
    "Cloud Security",
    "API Security",
    "OSINT",
    "Exploitation",
    "AI Systems",
    "Reporting",
    "Orchestration",
    "Infrastructure",
    "Plugin Systems",
    "CTF Automation",
    "Burp/MCP Integrations",
    "Intelligence/Correlation",
]

LANG_BY_EXT = {
    ".py": "Python",
    ".go": "Go",
    ".js": "JavaScript",
    ".jsx": "JavaScript/React",
    ".ts": "TypeScript",
    ".tsx": "TypeScript/React",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".ps1": "PowerShell",
    ".md": "Markdown",
    ".mdx": "Markdown/MDX",
    ".toml": "TOML",
    ".ini": "INI",
    ".cfg": "Config",
    ".conf": "Config",
    ".env": "Environment",
    ".txt": "Text",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "Sass",
    ".less": "Less",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".c": "C",
    ".h": "C/C++ Header",
    ".hpp": "C++ Header",
    ".cpp": "C++",
    ".cc": "C++",
    ".sql": "SQL",
    ".xml": "XML",
    ".tf": "Terraform",
    ".tfvars": "Terraform Vars",
    ".mod": "Go Module",
    ".sum": "Go Checksum",
    ".lock": "Lockfile",
    ".csv": "CSV",
    ".tsv": "TSV",
    ".png": "Image",
    ".jpg": "Image",
    ".jpeg": "Image",
    ".gif": "Image",
    ".svg": "SVG",
    ".webp": "Image",
    ".ico": "Image",
    ".pdf": "PDF",
    ".zip": "Archive",
    ".tar": "Archive",
    ".gz": "Archive",
    ".7z": "Archive",
    ".exe": "Binary",
    ".dll": "Binary",
    ".so": "Binary",
    ".dylib": "Binary",
    ".bin": "Binary",
}

TEXT_EXTS = {
    ".py",
    ".go",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".yaml",
    ".yml",
    ".json",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".md",
    ".mdx",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".env",
    ".txt",
    ".html",
    ".htm",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".vue",
    ".svelte",
    ".rs",
    ".java",
    ".kt",
    ".rb",
    ".php",
    ".cs",
    ".c",
    ".h",
    ".hpp",
    ".cpp",
    ".cc",
    ".sql",
    ".xml",
    ".tf",
    ".tfvars",
    ".mod",
    ".sum",
    ".lock",
    ".csv",
    ".tsv",
    ".dockerignore",
    ".gitignore",
    ".gitattributes",
    ".npmrc",
    ".prettierrc",
    ".eslintrc",
    ".babelrc",
    ".editorconfig",
    ".properties",
    ".gradle",
    ".proto",
    ".graphql",
}

CATEGORY_RULES = [
    (
        "Recon",
        [
            "subdomain",
            "dns",
            "asn",
            "whois",
            "asset",
            "recon",
            "crawl",
            "crawler",
            "wayback",
            "gau",
            "subfinder",
            "amass",
            "massdns",
            "shuffledns",
            "naabu",
            "httpx",
            "katana",
            "port scan",
            "enumerat",
        ],
    ),
    (
        "Web Scanning",
        [
            "nuclei",
            "dalfox",
            "xss",
            "fuzz",
            "ffuf",
            "gobuster",
            "dirsearch",
            "directory brute",
            "vulnerability scan",
            "web scan",
            "http probe",
            "wappalyzer",
            "whatweb",
            "template",
        ],
    ),
    (
        "Cloud Security",
        [
            "aws",
            "boto3",
            "s3",
            "iam",
            "azure",
            "gcp",
            "google cloud",
            "kubernetes",
            "kubectl",
            "k8s",
            "docker",
            "container",
            "terraform",
            "helm",
            "cloudtrail",
            "eks",
            "aks",
            "gke",
        ],
    ),
    (
        "API Security",
        [
            "graphql",
            "openapi",
            "swagger",
            "rest api",
            "api fuzz",
            "endpoint",
            "postman",
            "graphql schema",
            "jwt",
            "oauth",
        ],
    ),
    (
        "OSINT",
        [
            "osint",
            "phoneinfoga",
            "holehe",
            "sherlock",
            "email",
            "social",
            "username",
            "leak",
            "breach",
            "theharvester",
            "whois",
            "shodan",
            "censys",
        ],
    ),
    (
        "Exploitation",
        [
            "exploit",
            "sqli",
            "sql injection",
            "ssrf",
            "rce",
            "lfi",
            "rfi",
            "auth bypass",
            "payload",
            "privilege escalation",
            "metasploit",
            "cve-",
            "pwn",
        ],
    ),
    (
        "AI Systems",
        [
            "agent",
            "planner",
            "reasoning",
            "llm",
            "openai",
            "anthropic",
            "claude",
            "langchain",
            "llamaindex",
            "autonomous",
            "cognition",
            "prompt",
        ],
    ),
    (
        "Reporting",
        [
            "report",
            "markdown",
            "pdf",
            "html report",
            "dashboard",
            "summary",
            "chart",
            "visualization",
            "template",
            "export",
        ],
    ),
    (
        "Orchestration",
        [
            "workflow",
            "scheduler",
            "queue",
            "pipeline",
            "dag",
            "executor",
            "orchestr",
            "event bus",
            "pubsub",
            "worker",
            "task",
        ],
    ),
    (
        "Infrastructure",
        [
            "docker",
            "compose",
            "kubernetes",
            "helm",
            "terraform",
            "ci",
            "github actions",
            "gitlab-ci",
            "deployment",
            "environment",
            "config",
            "logging",
            "monitoring",
            "prometheus",
            "grafana",
        ],
    ),
    (
        "Plugin Systems",
        ["plugin", "adapter", "loader", "registry", "extension", "module system", "hook", "capability"],
    ),
    ("CTF Automation", ["ctf", "challenge", "pwn", "flag", "pwntools", "solve", "solver", "hackthebox", "tryhackme"]),
    (
        "Burp/MCP Integrations",
        ["burp", "mcp", "model context protocol", "fastmcp", "claude desktop", "proxy history"],
    ),
    (
        "Intelligence/Correlation",
        [
            "correlation",
            "graph",
            "relationship",
            "risk score",
            "risk scoring",
            "attack surface",
            "intelligence",
            "finding",
            "dedup",
            "enrichment",
            "neo4j",
        ],
    ),
]

TOOL_KEYWORDS = {
    "httpx": ["httpx"],
    "subfinder": ["subfinder"],
    "nuclei": ["nuclei"],
    "amass": ["amass"],
    "dalfox": ["dalfox"],
    "ffuf": ["ffuf"],
    "gobuster": ["gobuster"],
    "dirsearch": ["dirsearch"],
    "sqlmap": ["sqlmap"],
    "nmap": ["nmap"],
    "masscan": ["masscan"],
    "naabu": ["naabu"],
    "katana": ["katana"],
    "gau": ["gau", "getallurls"],
    "waybackurls": ["waybackurls", "wayback"],
    "dnsx": ["dnsx"],
    "tlsx": ["tlsx"],
    "shuffledns": ["shuffledns"],
    "massdns": ["massdns"],
    "whatweb": ["whatweb"],
    "wappalyzer": ["wappalyzer"],
    "trufflehog": ["trufflehog"],
    "gitleaks": ["gitleaks"],
    "phoneinfoga": ["phoneinfoga"],
    "holehe": ["holehe"],
    "sherlock": ["sherlock"],
    "theharvester": ["theharvester"],
    "metasploit": ["metasploit", "msfconsole", "msfvenom"],
    "burp": ["burp"],
    "mcp": ["mcp", "model context protocol"],
    "openai": ["openai"],
    "anthropic": ["anthropic", "claude"],
    "langchain": ["langchain"],
    "llamaindex": ["llamaindex"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "django": ["django"],
    "express": ["express"],
    "react": ["react"],
    "vite": ["vite"],
    "nextjs": ["next.js", "nextjs"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "kubectl", "k8s"],
    "terraform": ["terraform"],
    "aws": ["aws", "boto3", "s3"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "graphql": ["graphql"],
    "swagger": ["swagger"],
    "openapi": ["openapi"],
    "redis": ["redis"],
    "postgres": ["postgres", "postgresql"],
    "neo4j": ["neo4j"],
    "celery": ["celery"],
    "kafka": ["kafka"],
    "airflow": ["airflow"],
    "prefect": ["prefect"],
}

ENTRYPOINT_PATTERNS = {
    "cli": [
        r"if\s+__name__\s*==\s*['\"]__main__['\"]",
        r"argparse\.",
        r"click\.",
        r"typer\.",
        r"cobra\.",
        r"commander\.",
        r"process\.argv",
        r"func\s+main\s*\(",
        r"^#!.*(?:python|bash|sh|node|pwsh)",
    ],
    "api": [
        r"FastAPI\s*\(",
        r"Flask\s*\(",
        r"\bDjango\b",
        r"express\s*\(",
        r"uvicorn\.run",
        r"app\.listen\s*\(",
        r"http\.createServer",
        r"@app\.(get|post|put|delete|websocket)",
    ],
    "service": [r"\bcelery\b", r"\bworker\b", r"\bscheduler\b", r"while\s+True:", r"\bcron\b", r"\bqueue\b", r"\bconsumer\b", r"\bdaemon\b"],
    "mcp_server": [r"FastMCP", r"MCPServer", r"model context protocol", r"@modelcontextprotocol", r"from\s+mcp\b", r"import\s+mcp\b"],
    "dashboard": [r"\bReact\b", r"createRoot", r"\bVite\b", r"\bnext\s", r"\sstreamlit\b", r"\bgradio\b", r"\bdash\.", r"\bDashboard\b"],
}

IMPORT_RE_JS = re.compile(
    r"(?:import\s+(?:[^;]+?)\s+from\s+['\"]([^'\"]+)['\"]|require\s*\(\s*['\"]([^'\"]+)['\"]\s*\))"
)
GO_IMPORT_BLOCK_RE = re.compile(r"import\s*\((.*?)\)", re.S)
GO_IMPORT_SINGLE_RE = re.compile(r"import\s+['\"]([^'\"]+)['\"]")
REQ_LINE_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+)\s*([<>=!~]=?\s*[^;#\s]+)?")
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_+.-]{2,}")
SAMPLE_LIMIT = 120_000
TEXT_CACHE_LIMIT = 2_000_000
PREFIX_KEYWORDS = {"enumerat", "orchestr"}


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(BASE)).replace("\\", "/")
    except ValueError:
        return str(path.resolve()).replace("\\", "/")


def source_root(path: Path) -> str:
    for root in SOURCE_ROOTS:
        try:
            path.resolve().relative_to(root.resolve())
            return root.name
        except ValueError:
            pass
    return ""


def language_for(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if name == "dockerfile" or name.endswith(".dockerfile"):
        return "Dockerfile"
    if name in {"makefile", "gnumakefile"}:
        return "Makefile"
    if name == "go.mod":
        return "Go Module"
    if name == "go.sum":
        return "Go Checksum"
    if name.startswith(".") and not suffix:
        return "Config"
    return LANG_BY_EXT.get(suffix, "Unknown/Binary")


def probably_text(path: Path, prefix: bytes) -> bool:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if language_for(path) in {"Dockerfile", "Makefile", "Go Module", "Go Checksum"}:
        return True
    if suffix in TEXT_EXTS or name in {"requirements.txt", "package.json", "pyproject.toml"}:
        return True
    if b"\x00" in prefix:
        return False
    if not prefix:
        return True
    printable = sum(1 for b in prefix if b in b"\n\r\t" or 32 <= b < 127)
    return printable / len(prefix) > 0.85


def read_text(path: Path) -> tuple[str, str, bool]:
    try:
        size = path.stat().st_size
        raw = path.read_bytes()[:SAMPLE_LIMIT] if size > TEXT_CACHE_LIMIT else path.read_bytes()
        truncated = size > TEXT_CACHE_LIMIT
        for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
            try:
                return raw.decode(encoding), encoding, truncated
            except UnicodeDecodeError:
                continue
        return raw.decode("utf-8", errors="replace"), "utf-8-replace", truncated
    except Exception as exc:  # pragma: no cover - diagnostic artifact
        return "", f"read-error:{exc.__class__.__name__}", False


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception as exc:  # pragma: no cover - diagnostic artifact
        return f"error:{exc.__class__.__name__}"


def python_imports(text: str) -> list[str]:
    imports: set[str] = set()
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
    except SyntaxError:
        for match in re.finditer(r"^\s*(?:from\s+([A-Za-z0-9_.]+)\s+import|import\s+([A-Za-z0-9_.]+))", text, re.M):
            imports.add((match.group(1) or match.group(2)).split(".")[0])
    return sorted(imports)


def js_imports(text: str) -> list[str]:
    deps: set[str] = set()
    for first, second in IMPORT_RE_JS.findall(text):
        dep = first or second
        if not dep or dep.startswith("."):
            continue
        deps.add("/".join(dep.split("/")[:2]) if dep.startswith("@") else dep.split("/")[0])
    return sorted(deps)


def go_imports(text: str) -> list[str]:
    deps: set[str] = set()
    for block in GO_IMPORT_BLOCK_RE.findall(text):
        deps.update(re.findall(r"['\"]([^'\"]+)['\"]", block))
    deps.update(GO_IMPORT_SINGLE_RE.findall(text))
    return sorted(deps)


def manifest_dependencies(path: Path, text: str) -> list[dict[str, Any]]:
    name = path.name.lower()
    deps: list[dict[str, Any]] = []
    if "requirements" in name and name.endswith(".txt"):
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("-"):
                continue
            match = REQ_LINE_RE.match(stripped)
            if match:
                deps.append({"name": match.group(1).lower(), "specifier": (match.group(2) or "").replace(" ", ""), "source": rel(path)})
    elif name == "package.json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {}
        for section in ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]:
            for dep_name, version in (data.get(section) or {}).items():
                deps.append({"name": dep_name.lower(), "specifier": str(version), "source": rel(path), "section": section})
    elif name == "go.mod":
        for match in re.finditer(r"^\s*([A-Za-z0-9_.\-/]+)\s+(v[^\s]+)", text, re.M):
            dep_name = match.group(1)
            if "." in dep_name or "/" in dep_name:
                deps.append({"name": dep_name.lower(), "specifier": match.group(2), "source": rel(path)})
    elif name == "pyproject.toml":
        for match in re.finditer(r"['\"]([A-Za-z0-9_.-]+(?:[<>=!~]=?[^'\"]+)?)\s*['\"]", text):
            dep = match.group(1)
            if any(op in dep for op in [">=", "==", "<=", "~=", ">", "<"]):
                dep_name = re.split(r"[<>=!~]", dep, 1)[0].strip().lower()
                deps.append({"name": dep_name, "specifier": dep[len(dep_name) :], "source": rel(path)})
    return deps


def related_tools_for(blob: str) -> list[str]:
    lower = blob.lower()
    return sorted(tool for tool, patterns in TOOL_KEYWORDS.items() if any(keyword_present(lower, pattern) for pattern in patterns))


def keyword_present(blob: str, keyword: str) -> bool:
    keyword = keyword.lower()
    if keyword in PREFIX_KEYWORDS:
        return keyword in blob
    if re.fullmatch(r"[a-z0-9_]+", keyword):
        return re.search(rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])", blob) is not None
    return keyword in blob


def classify(path: Path, text: str, language: str, related_tools: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    blob = f"{path.name}\n{rel(path)}\n{text[:SAMPLE_LIMIT]}".lower()
    categories: list[str] = []
    evidence: dict[str, list[str]] = {}
    for category, keywords in CATEGORY_RULES:
        hits = sorted({keyword for keyword in keywords if keyword_present(blob, keyword)})
        if hits:
            categories.append(category)
            evidence[category] = hits[:8]
    if any(tool in related_tools for tool in ["httpx", "subfinder", "amass", "dnsx", "tlsx", "naabu", "katana", "gau", "waybackurls"]):
        if "Recon" not in categories:
            categories.insert(0, "Recon")
    if any(tool in related_tools for tool in ["nuclei", "dalfox", "ffuf", "gobuster", "dirsearch", "sqlmap", "whatweb", "wappalyzer"]):
        if "Web Scanning" not in categories:
            categories.insert(0, "Web Scanning")
    if categories:
        return categories, evidence
    if language in {"Dockerfile", "Terraform", "YAML", "JSON", "TOML", "Config", "Environment", "INI"}:
        return ["Infrastructure"], {"Infrastructure": ["config/runtime artifact"]}
    if language in {"Markdown", "Markdown/MDX", "PDF", "Image", "SVG"}:
        return ["Reporting"], {"Reporting": ["documentation or visual artifact"]}
    return ["Infrastructure"], {"Infrastructure": ["uncategorized support artifact"]}


def entrypoints_for(text: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for entry_type, patterns in ENTRYPOINT_PATTERNS.items():
        signals = [pattern for pattern in patterns if re.search(pattern, text, re.I | re.M)]
        if signals:
            entries.append({"type": entry_type, "signals": signals[:6]})
    return entries


def execution_type_for(path: Path, text: str, language: str, categories: list[str]) -> str:
    blob = f"{path.name}\n{rel(path)}\n{text[:50_000]}".lower()
    name = path.name.lower()
    if language in {"Image", "PDF", "Archive", "Binary"}:
        return "binary/data"
    if any(marker in blob for marker in ["test_", "_test.", "/tests/", "\\tests\\", ".spec.", ".test."]):
        return "test"
    if name == "dockerfile" or "docker-compose" in name or name in {"compose.yml", "compose.yaml"}:
        return "runtime/deployment"
    if language in {"YAML", "JSON", "TOML", "Config", "INI", "Environment", "Terraform", "Go Module", "Go Checksum", "Lockfile"}:
        return "workflow/config" if any(word in blob for word in ["workflow", "github actions", "pipeline", "ci"]) else "configuration"
    entries = entrypoints_for(text)
    if entries:
        priority = ["mcp_server", "api", "dashboard", "service", "cli"]
        found = {entry["type"] for entry in entries}
        return next(kind for kind in priority if kind in found)
    if any(word in blob for word in ["adapter", "wrapper"]):
        return "adapter"
    if "plugin" in blob:
        return "plugin"
    if "dashboard" in blob or language in {"JavaScript/React", "TypeScript/React", "Vue", "Svelte"}:
        return "dashboard"
    if language in {"Markdown", "Markdown/MDX"}:
        return "documentation"
    if language in {"Shell", "PowerShell"}:
        return "cli/script"
    return "library"


def normalized_stem(path: Path) -> str:
    stem = path.stem.lower()
    stem = re.sub(r"(_copy| copy| - copy|\.bak|\.old|\.orig)$", "", stem)
    stem = re.sub(r"[_\-. ]+(v?\d+|final|new|old|backup|bak|copy|latest)$", "", stem)
    stem = re.sub(r"[_\-. ]+", "_", stem).strip("_")
    return stem or path.stem.lower()


def token_fingerprint(text: str) -> str:
    tokens = [token.lower() for token in TOKEN_RE.findall(text[:SAMPLE_LIMIT])]
    stop = {"the", "and", "for", "with", "from", "this", "that", "return", "class", "function", "import", "const", "var", "let", "def", "true", "false", "none", "null"}
    useful = sorted({token for token in tokens if token not in stop})
    if not useful:
        return ""
    return hashlib.sha1(" ".join(useful[:1500]).encode("utf-8", "ignore")).hexdigest()


def purpose_for(
    language: str,
    categories: list[str],
    execution_type: str,
    related_tools: list[str],
    dependencies: list[str],
    entrypoints: list[dict[str, Any]],
) -> str:
    tool_text = f"; references {', '.join(related_tools[:8])}" if related_tools else ""
    dep_text = f"; key deps: {', '.join(dependencies[:6])}" if dependencies else ""
    entry_text = f"; entrypoints: {', '.join(entry['type'] for entry in entrypoints[:4])}" if entrypoints else ""
    return f"{language} {execution_type.replace('_', ' ')} for {', '.join(categories[:3])}{tool_text}{dep_text}{entry_text}."


def importance_for(path: Path, categories: list[str], execution_type: str, related_tools: list[str]) -> str:
    blob = f"{path.name}/{rel(path)}".lower()
    if execution_type in {"workflow/config", "api", "service", "mcp_server"}:
        return "high"
    if any(category in categories for category in ["Orchestration", "Plugin Systems", "Intelligence/Correlation", "AI Systems"]) and execution_type not in {"documentation", "test"}:
        return "high"
    if related_tools and execution_type not in {"documentation", "test"}:
        return "medium-high"
    if execution_type in {"test", "documentation", "binary/data"} or any(word in blob for word in ["example", "sample", "demo", "fixture", "screenshot", "gif"]):
        return "low"
    return "medium"


def orchestration_relevance(path: Path, categories: list[str], execution_type: str) -> str:
    blob = f"{path.name}/{rel(path)}".lower()
    if "Orchestration" in categories or any(word in blob for word in ["workflow", "executor", "scheduler", "event", "queue", "pipeline"]):
        return "high"
    if execution_type in {"api", "service", "workflow/config", "plugin", "adapter", "mcp_server"}:
        return "medium-high"
    if any(category in categories for category in ["Plugin Systems", "AI Systems", "Intelligence/Correlation"]):
        return "medium"
    return "low"


def reusable_logic(language: str, execution_type: str, importance: str) -> str:
    if execution_type in {"binary/data", "documentation", "test", "configuration"}:
        return "reference_only"
    if importance in {"high", "medium-high"}:
        return "candidate_for_adapter_or_native_module"
    if language in {"Python", "Go", "JavaScript", "TypeScript", "Shell", "PowerShell"}:
        return "review_for_extraction"
    return "low_reuse"


def write_json(name: str, data: Any) -> None:
    path = OUT / name
    tmp = OUT / f".{name}.tmp"
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    try:
        tmp.replace(path)
    except PermissionError:
        # Some desktop indexers/editors keep large JSON artifacts open on
        # Windows and block atomic replacement. A direct overwrite still keeps
        # the required canonical filename fresh in that case.
        path.write_text(tmp.read_text(encoding="utf-8"), encoding="utf-8")
        tmp.unlink(missing_ok=True)


def count_table(counter: dict[str, int], rows: int = 20) -> str:
    lines = ["| Name | Count |", "|---|---:|"]
    for name, count in list(counter.items())[:rows]:
        lines.append(f"| {name} | {count} |")
    return "\n".join(lines)


def analyze() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = sorted(
        [path for root in SOURCE_ROOTS if root.exists() for path in root.rglob("*") if path.is_file()],
        key=lambda item: rel(item).lower(),
    )

    inventory: list[dict[str, Any]] = []
    entrypoint_records: list[dict[str, Any]] = []
    manifest_deps: list[dict[str, Any]] = []
    file_dep_graph: dict[str, Any] = {}
    hash_groups: dict[str, list[str]] = collections.defaultdict(list)
    stem_groups: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    fingerprint_groups: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    dep_usage: dict[str, list[str]] = collections.defaultdict(list)
    category_counts: collections.Counter[str] = collections.Counter()
    errors: list[dict[str, str]] = []

    for path in paths:
        try:
            stat = path.stat()
            with path.open("rb") as handle:
                prefix = handle.read(4096)
            language = language_for(path)
            textish = probably_text(path, prefix)
            text, encoding, truncated = ("", "binary", False)
            if textish:
                text, encoding, truncated = read_text(path)

            digest = sha256_file(path)
            hash_groups[digest].append(rel(path))
            stem_groups[(normalized_stem(path), path.suffix.lower())].append(rel(path))
            if text:
                fingerprint = token_fingerprint(text)
                if fingerprint:
                    fingerprint_groups[(fingerprint, path.suffix.lower())].append(rel(path))

            deps: list[str] = []
            if language == "Python":
                deps = python_imports(text)
            elif language in {"JavaScript", "JavaScript/React", "TypeScript", "TypeScript/React", "Vue", "Svelte"}:
                deps = js_imports(text)
            elif language == "Go":
                deps = go_imports(text)

            mdeps = manifest_dependencies(path, text) if text else []
            manifest_deps.extend(mdeps)
            for dep in deps:
                dep_usage[dep.lower()].append(rel(path))
            for dep in mdeps:
                dep_usage[dep["name"].lower()].append(rel(path))

            blob = f"{path.name}\n{rel(path)}\n{text[:SAMPLE_LIMIT]}"
            related_tools = related_tools_for(blob if textish else f"{path.name}\n{rel(path)}")
            categories, evidence = classify(path, text, language, related_tools)
            for category in categories:
                category_counts[category] += 1
            entrypoints = entrypoints_for(text) if text else []
            execution_type = execution_type_for(path, text, language, categories)

            for entry in entrypoints:
                entrypoint_records.append(
                    {
                        "file": path.name,
                        "path": rel(path),
                        "absolute_path": str(path.resolve()),
                        "type": entry["type"],
                        "language": language,
                        "signals": entry["signals"],
                        "source_root": source_root(path),
                        "command_hint": None,
                    }
                )

            dep_names = deps or [dep["name"] for dep in mdeps]
            item = {
                "filename": path.name,
                "path": str(path.resolve()),
                "relative_path": rel(path),
                "source_root": source_root(path),
                "language": language,
                "purpose": purpose_for(language, categories, execution_type, related_tools, dep_names, entrypoints),
                "category": categories,
                "category_evidence": evidence,
                "dependencies": deps,
                "manifest_dependencies": mdeps[:10],
                "execution_type": execution_type,
                "related_tools": related_tools,
                "importance": "",
                "reusable_logic": "",
                "orchestration_relevance": "",
                "size_bytes": stat.st_size,
                "sha256": digest,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "encoding": encoding,
                "content_truncated": truncated,
                "entrypoint_signals": entrypoints,
            }
            item["importance"] = importance_for(path, categories, execution_type, related_tools)
            item["reusable_logic"] = reusable_logic(language, execution_type, item["importance"])
            item["orchestration_relevance"] = orchestration_relevance(path, categories, execution_type)
            inventory.append(item)
            file_dep_graph[rel(path)] = {
                "language": language,
                "dependencies": deps,
                "manifest_dependencies": mdeps,
                "related_tools": related_tools,
                "categories": categories,
            }
        except Exception as exc:  # pragma: no cover - diagnostic artifact
            errors.append({"path": rel(path), "error": repr(exc)})

    exact_duplicates = [
        {"sha256": digest, "count": len(group), "files": sorted(group)}
        for digest, group in hash_groups.items()
        if len(group) > 1 and not digest.startswith("error:")
    ]
    exact_duplicates.sort(key=lambda item: (-item["count"], item["files"][0]))

    renamed_variants = [
        {"normalized_name": stem, "extension": ext, "count": len(group), "files": sorted(group)}
        for (stem, ext), group in stem_groups.items()
        if len(group) > 1
    ]
    renamed_variants.sort(key=lambda item: (-item["count"], item["normalized_name"]))

    near_duplicates = [
        {"fingerprint": fingerprint, "extension": ext, "count": len(group), "files": sorted(group)}
        for (fingerprint, ext), group in fingerprint_groups.items()
        if len(group) > 1
    ]
    near_duplicates.sort(key=lambda item: (-item["count"], item["files"][0]))

    capability_matrix = build_capability_matrix(inventory, category_counts)
    dependency_graph = build_dependency_graph(file_dep_graph, dep_usage, manifest_deps, errors)
    execution_entrypoints = build_entrypoints(entrypoint_records)
    duplicate_map = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_files": len(inventory),
            "exact_duplicate_groups": len(exact_duplicates),
            "renamed_or_variant_groups": len(renamed_variants),
            "near_duplicate_text_groups": len(near_duplicates),
        },
        "exact_duplicates": exact_duplicates,
        "renamed_or_variant_groups": renamed_variants,
        "near_duplicate_text_groups": near_duplicates,
        "policy": "Do not delete originals. Use this map to choose one reviewed implementation per capability and migrate through adapters only.",
    }

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_roots": [str(root.resolve()) for root in SOURCE_ROOTS],
        "total_files": len(inventory),
        "text_or_source_files": sum(1 for item in inventory if item["encoding"] != "binary"),
        "binary_or_data_files": sum(1 for item in inventory if item["encoding"] == "binary"),
        "category_counts": dict(category_counts.most_common()),
        "language_counts": dict(collections.Counter(item["language"] for item in inventory).most_common()),
        "execution_type_counts": dict(collections.Counter(item["execution_type"] for item in inventory).most_common()),
        "analysis_errors": errors,
    }

    write_json("tool_inventory.json", inventory)
    write_json("capability_matrix.json", capability_matrix)
    write_json("duplicate_map.json", duplicate_map)
    write_json("dependency_graph.json", dependency_graph)
    write_json("execution_entrypoints.json", execution_entrypoints)
    write_json("stage1_analysis_summary.json", summary)
    (OUT / "architecture_plan.md").write_text(render_architecture_plan(summary), encoding="utf-8")
    (OUT / "migration_plan.md").write_text(render_migration_plan(summary), encoding="utf-8")

    return {
        "files_analyzed": len(inventory),
        "errors": len(errors),
        "categories": summary["category_counts"],
        "exact_duplicate_groups": len(exact_duplicates),
        "variant_groups": len(renamed_variants),
        "near_duplicate_groups": len(near_duplicates),
        "entrypoints": execution_entrypoints["entrypoint_count"],
    }


def build_capability_matrix(inventory: list[dict[str, Any]], category_counts: collections.Counter[str]) -> list[dict[str, Any]]:
    strengths = {
        "Recon": "Broad asset discovery coverage: DNS, subdomains, HTTP probing, crawling, and network enumeration.",
        "Web Scanning": "Strong vulnerability/template scanning, fuzzing, XSS, HTTP fingerprinting, and web surface discovery overlap.",
        "Cloud Security": "Cloud/container/IaC artifacts across Docker, Kubernetes, Terraform, and cloud SDK usage.",
        "API Security": "API endpoint discovery, OpenAPI/Swagger/GraphQL parsing, JWT/auth helpers, and service code.",
        "OSINT": "Email, username, phone, breach, and public intelligence tooling appears in reusable scripts.",
        "Exploitation": "Exploit and payload scripts exist but should be governed and isolated before activation.",
        "AI Systems": "Large agent/planner/LLM surface with MCP/OpenAI/Claude integrations for future planning.",
        "Reporting": "Dashboards, markdown/HTML/PDF reporting assets, and visualization components.",
        "Orchestration": "Workflow, queue, executor, scheduler, and event abstractions are present.",
        "Infrastructure": "Deployment, container, CI, config, environment, and observability assets.",
        "Plugin Systems": "Adapter/registry/loader patterns that should converge into one ReconX plugin contract.",
        "CTF Automation": "Challenge solvers and exploit chains are useful as optional plugins, not core logic.",
        "Burp/MCP Integrations": "Burp and MCP bridge code can become optional operator integrations.",
        "Intelligence/Correlation": "Graph, scoring, deduplication, enrichment, and finding models for intelligence.",
    }
    primary_hints = {
        "Recon": ["httpx", "subfinder", "amass", "dnsx", "katana"],
        "Web Scanning": ["nuclei", "dalfox", "ffuf", "dirsearch"],
        "Cloud Security": ["kubernetes", "docker", "aws", "terraform"],
        "API Security": ["openapi", "swagger", "graphql"],
        "OSINT": ["holehe", "phoneinfoga", "sherlock", "theharvester"],
        "Exploitation": ["sqlmap", "metasploit"],
        "AI Systems": ["openai", "anthropic", "langchain", "mcp"],
        "Reporting": ["react", "vite", "dashboard"],
        "Orchestration": ["workflow_engine", "executor", "event_bus", "scheduler"],
        "Infrastructure": ["docker", "kubernetes", "terraform", "github_workflows"],
        "Plugin Systems": ["plugin_loader", "adapter", "registry"],
        "CTF Automation": ["ctf", "solver"],
        "Burp/MCP Integrations": ["burp", "mcp"],
        "Intelligence/Correlation": ["correlation", "neo4j", "risk_scorer", "risk", "finding"],
    }
    clusters_by_category: dict[str, dict[str, Any]] = {category: {} for category in REQUIRED_CATEGORIES}
    for item in inventory:
        names = item["related_tools"] or [normalized_stem(Path(item["filename"]))]
        for category in item["category"]:
            bucket = clusters_by_category.setdefault(category, {})
            for name in names[:4]:
                cluster = bucket.setdefault(
                    name,
                    {
                        "name": name,
                        "file_count": 0,
                        "languages": set(),
                        "execution_types": collections.Counter(),
                        "sample_paths": [],
                        "importance_counts": collections.Counter(),
                        "related_tools": set(),
                    },
                )
                cluster["file_count"] += 1
                cluster["languages"].add(item["language"])
                cluster["execution_types"][item["execution_type"]] += 1
                cluster["importance_counts"][item["importance"]] += 1
                cluster["related_tools"].update(item["related_tools"])
                if len(cluster["sample_paths"]) < 8:
                    cluster["sample_paths"].append(item["relative_path"])

    matrix: list[dict[str, Any]] = []
    for category in REQUIRED_CATEGORIES:
        tools = []
        for cluster in clusters_by_category.get(category, {}).values():
            tools.append(
                {
                    "name": cluster["name"],
                    "file_count": cluster["file_count"],
                    "languages": sorted(cluster["languages"]),
                    "execution_types": dict(cluster["execution_types"].most_common()),
                    "sample_paths": cluster["sample_paths"],
                    "importance_counts": dict(cluster["importance_counts"].most_common()),
                    "related_tools": sorted(cluster["related_tools"]),
                }
            )
        tools.sort(key=lambda item: (-item["file_count"], item["name"]))
        overlaps = []
        for other in REQUIRED_CATEGORIES:
            if other == category:
                continue
            shared = sum(1 for item in inventory if category in item["category"] and other in item["category"])
            if shared:
                overlaps.append({"category": other, "shared_file_count": shared})
        overlaps.sort(key=lambda item: -item["shared_file_count"])
        recommended = None
        for hint in primary_hints[category]:
            match = next((tool for tool in tools if candidate_name_matches(tool["name"], hint)), None)
            if match:
                recommended = {
                    "name": match["name"],
                    "reason": f"Highest-priority known candidate for {category}; wrap via ReconX adapter contract before native migration.",
                    "sample_paths": match["sample_paths"][:5],
                }
                break
        if recommended is None and tools:
            recommended = {
                "name": tools[0]["name"],
                "reason": f"Largest detected implementation cluster for {category}; requires manual quality review before promotion.",
                "sample_paths": tools[0]["sample_paths"][:5],
            }
        matrix.append(
            {
                "category": category,
                "file_count": category_counts.get(category, 0),
                "tools": tools,
                "strengths": strengths[category],
                "overlaps": overlaps[:10],
                "recommended_primary_implementation": recommended,
            }
        )
    return matrix


def candidate_name_matches(name: str, hint: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    hint_normalized = re.sub(r"[^a-z0-9]+", "_", hint.lower()).strip("_")
    tokens = [token for token in normalized.split("_") if token]
    return normalized == hint_normalized or hint_normalized in tokens


def build_dependency_graph(
    file_dep_graph: dict[str, Any],
    dep_usage: dict[str, list[str]],
    manifest_deps: list[dict[str, Any]],
    errors: list[dict[str, str]],
) -> dict[str, Any]:
    runtime_dependencies = {
        dep: {"count": len(paths), "files": sorted(set(paths))[:25]}
        for dep, paths in sorted(dep_usage.items(), key=lambda item: (-len(item[1]), item[0]))
    }
    version_specs: dict[str, set[str]] = collections.defaultdict(set)
    version_sources: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    for dep in manifest_deps:
        name = dep["name"].lower()
        specifier = dep.get("specifier") or ""
        if specifier:
            version_specs[name].add(specifier)
            version_sources[name].append({"specifier": specifier, "source": dep.get("source", "")})
    conflicts = []
    for name, specs in version_specs.items():
        exacts = {spec for spec in specs if spec.startswith("==") or re.match(r"^\d", spec)}
        if len(specs) > 2 or len(exacts) > 1:
            conflicts.append({"dependency": name, "specifiers": sorted(specs), "sources": version_sources[name][:20]})
    conflicts.sort(key=lambda item: item["dependency"])
    shared = [
        {"dependency": dep, "file_count": info["count"], "sample_files": info["files"][:10]}
        for dep, info in runtime_dependencies.items()
        if info["count"] >= 2
    ]
    shared.sort(key=lambda item: (-item["file_count"], item["dependency"]))
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_roots": [str(root.resolve()) for root in SOURCE_ROOTS],
        "file_count": len(file_dep_graph),
        "files": file_dep_graph,
        "runtime_dependencies": runtime_dependencies,
        "shared_libraries": shared,
        "conflicting_packages": conflicts,
        "manifest_dependency_records": manifest_deps,
        "analysis_errors": errors,
    }


def build_entrypoints(records: list[dict[str, Any]]) -> dict[str, Any]:
    for record in records:
        path = record["path"]
        language = record["language"]
        if record["type"] == "cli":
            if language == "Python":
                record["command_hint"] = f"python {path}"
            elif language == "Go":
                record["command_hint"] = f"go run {path}"
            elif language.startswith(("JavaScript", "TypeScript")):
                record["command_hint"] = f"node {path}"
            elif language in {"Shell", "PowerShell"}:
                record["command_hint"] = path
        elif record["type"] == "api":
            record["command_hint"] = "review framework-specific server invocation"
        elif record["type"] == "dashboard":
            record["command_hint"] = "review package scripts / frontend dev server"
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "entrypoint_count": len(records),
        "entrypoints": sorted(records, key=lambda item: (item["type"], item["path"])),
        "by_type": dict(collections.Counter(record["type"] for record in records).most_common()),
    }


def render_architecture_plan(summary: dict[str, Any]) -> str:
    return f"""# ReconX Architecture Plan: Stage 1 Capability Map

Generated: {summary["generated_at"]}

## Scope

This stage inspected `{summary["total_files"]}` files from the read-only source roots:

- `{SOURCE_ROOTS[0].resolve()}`
- `{SOURCE_ROOTS[1].resolve()}`

No files in `pccc` or `allfiles` were modified. The generated intelligence artifacts are designed to support the activation prompt's thin vertical slice without turning ReconX into a bulk-merged monolith.

## Capability Distribution

{count_table(summary["category_counts"])}

## Runtime / Language Distribution

{count_table(summary["language_counts"])}

## Execution Role Distribution

{count_table(summary["execution_type_counts"])}

## Target ReconX Structure

ReconX should remain a narrow core surrounded by isolated capabilities:

- `core/`: execution manager, sandbox contracts, structured logging, cancellation, retries, and timeout handling.
- `orchestration/`: workflow DAG parsing, dependency resolution, checkpoints, and scheduling.
- `events/`: async event bus, event history, websocket fan-out, and telemetry routing.
- `plugins/`: capability plugins grouped by domain, each exposing `run(target, options) -> normalized_results`.
- `adapters/`: subprocess, container, API, and library adapters that isolate external tools.
- `normalization/`: schemas, deduplication, confidence scoring, enrichment, and timestamping.
- `correlation/`: target grouping, technology correlation, attack-surface links, and risk scoring.
- `governance/`: target validation, plugin allow/deny controls, audit trail, and policy decisions.
- `api/`: FastAPI gateway for workflow launch, status, plugin listing, health, and telemetry streams.
- `dashboard/`: React/Vite operator UI consuming API and websocket events.
- `deployment/`: Docker Compose, Kubernetes, Helm, and environment validation.
- `testing/`: unit and integration tests for the thin vertical slice.

## Plugin Architecture

All imported capability code should be converted into ReconX plugins rather than copied directly. The standard plugin contract should be:

```python
async def run(target: str, options: dict) -> list[dict]:
    ...
```

Each plugin package should include `manifest.json`, `adapter.py`, input/output schemas, parser fixtures, and tests. External tools such as `httpx`, `subfinder`, `nuclei`, and `amass` should remain external runtime dependencies until their adapters prove stable.

## First Operational Flow

1. CLI/API receives `quick_recon` and a target.
2. Governance validates target and plugin permissions.
3. Workflow engine parses `workflows/quick_recon.yaml` into a DAG.
4. Executor dispatches the `httpx` plugin through its adapter sandbox.
5. Adapter captures stdout/stderr, exit status, runtime, and timeout state.
6. Normalization emits unified findings.
7. Correlation groups findings by target and computes an initial risk score.
8. Event bus publishes workflow, plugin, finding, and policy events.
9. FastAPI exposes workflow state and websocket telemetry.
10. Dashboard renders progress, timeline, logs, and findings count.

## Recommended Thin Slice

- `events/event_bus.py` or `events/bus.py`: async pub/sub with event history and websocket subscribers.
- `core/execution/executor.py` or `core/execution_manager.py`: asyncio execution, retries, cancellation, timeout, telemetry.
- `orchestration/workflow_engine.py`: YAML DAG traversal and dependency resolution.
- `core/plugin_loader.py`: manifest discovery, adapter binding, dependency validation.
- `plugins/recon/httpx/adapter.py`: first real subprocess adapter.
- `normalization/pipeline.py`: unified finding schema and deduplication.
- `correlation/engine.py`: target grouping and baseline risk scoring.
- `governance/policy_engine.py`: execution permission checks and audit logging.
- `api/gateway/main.py`: workflow launch, status, plugin list, health, websocket stream.
- `dashboard/`: React/Vite live telemetry view.

## Governance and Isolation

- Source roots remain read-only reference material.
- Plugins run behind adapters with explicit timeouts and captured output.
- Policy gates every workflow before execution and every plugin before dispatch.
- Events are structured, timestamped, and auditable.
- Findings are normalized before they enter correlation or reporting.
- Exploitation and CTF tools remain disabled until explicit governance policies exist.
"""


def render_migration_plan(summary: dict[str, Any]) -> str:
    return f"""# ReconX Migration Plan: Stage 1

Generated: {summary["generated_at"]}

## Migration Rule

Do not bulk-merge repositories. `pccc` is the original source of truth and `allfiles` is an extraction lake. ReconX should ingest ideas, contracts, parser logic, and adapter candidates only after review.

## What Moves Into ReconX Core

- Async execution primitives: retries, cancellation, timeout, and structured telemetry.
- Workflow/DAG parsing and scheduling code that can be tested independently.
- Event bus logic with pub/sub, history, and websocket fan-out.
- Normalization schemas and deduplication helpers.
- Correlation/risk-scoring logic that operates on normalized findings.
- Governance policy checks for target scope, plugin allowlists, and audit records.

These should be rewritten cleanly when existing files are scaffold-heavy or tightly coupled.

## What Becomes Plugins

- Recon: `httpx`, `subfinder`, `amass`, DNS/ASN/crawling tools.
- Web Scanning: `nuclei`, `dalfox`, fuzzers, directory brute force, parameter discovery.
- Cloud Security: AWS/Azure/GCP/Kubernetes/Docker analyzers.
- API Security: GraphQL, OpenAPI/Swagger, REST enumeration and fuzzing.
- OSINT: email, phone, username, and breach intelligence tools.
- Reporting: markdown/HTML/PDF/report generators and dashboard widgets.
- Burp/MCP: optional operator integrations, not core dependencies.

Every plugin should provide a manifest, adapter, parser fixtures, and a normalized output schema.

## What Remains External

- Go security binaries and large third-party scanners.
- Standalone dashboards that do not share the ReconX API contract.
- Deployment stacks that target a different product topology.
- Heavy AI agent frameworks until the base execution path is stable.
- Exploitation and CTF chains until governance can enforce explicit authorization.

## What Should Be Deprecated

- Exact duplicates and renamed copies listed in `duplicate_map.json`.
- Experimental forks with no unique parser or adapter value.
- Monolithic scripts that mix scanning, UI, storage, and reporting.
- Old screenshots, generated assets, demos, and stale examples.
- Direct subprocess calls embedded in business logic without isolation.

## First Activation Migration Order

1. Implement core event bus, executor, and workflow engine from clean interfaces.
2. Add `quick_recon.yaml` as the first workflow.
3. Add only the `httpx` adapter and manifest.
4. Normalize `httpx` output into unified findings.
5. Add baseline correlation and target grouping.
6. Gate execution through policy engine.
7. Expose workflow state through FastAPI and websocket telemetry.
8. Connect dashboard telemetry after API events are stable.
9. Add tests for executor, workflow DAG, policy, adapter parsing, normalization, and API.
10. Add CI after local tests are green.

## Candidate Selection Heuristics

Prefer candidates with focused responsibility, tests or fixtures, clear CLI/API boundaries, minimal hardcoded environment assumptions, structured output, recent modification time, fewer duplicate variants, and no embedded credentials or unsafe side effects.

## Review Queues

- Start with high-importance, high-orchestration files in `tool_inventory.json`.
- Use `capability_matrix.json` to pick one primary per category.
- Use `duplicate_map.json` to avoid migrating forks or renamed copies.
- Use `dependency_graph.json` before adding dependencies.
- Use `execution_entrypoints.json` to identify code that can become service adapters or CLI plugins.
"""


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2))
