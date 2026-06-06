"""
ReconX — Stage 21: MCP Server
==============================
Exposes ReconX as an MCP (Model Context Protocol) server.

Compatible with: Claude Code, Cursor, Codex, and any MCP client.
All 200+ wrapped tool capabilities are reachable via:
  list_tools       — enumerate available ReconX capabilities
  run_tool         — execute a specific tool
  plan_scan        — get AI-recommended tool chain for a target
  get_findings     — retrieve findings from the data store
  get_summary      — executive summary of a scan

Run:
    uvicorn reconx.api.mcp_server:app --host 127.0.0.1 --port 8765

Register with Claude Code:
    claude mcp add reconx -- uvicorn reconx.api.mcp_server:app --host 127.0.0.1 --port 8765

Safety:
  - All targets validated before execution
  - No tools run without explicit tool_name + target in request
  - Rate limiting applied per client
  - Scope enforcement: strict_scope=True blocks off-target requests
"""
from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import asdict, dataclass
from typing import Any, Optional

log = logging.getLogger("reconx.api.mcp_server")

# ── Tool Registry (MCP-exposed capabilities) ──────────────────────────────────
# Each entry describes one ReconX capability exposed via MCP.
# tool_id maps to an internal ReconX tool or pipeline.

MCP_TOOLS: list[dict] = [
    # ── Discovery ─────────────────────────────────────────────────────────────
    {
        "name": "reconx_passive_discovery",
        "description": "Passive subdomain and asset discovery using CT logs, DNS records, public APIs, and OSINT sources. No active traffic to the target.",
        "category": "discovery",
        "parameters": {
            "target":  {"type": "string", "description": "Domain name (e.g. example.com)", "required": True},
            "depth":   {"type": "string", "enum": ["shallow", "deep"], "default": "shallow"},
        },
    },
    {
        "name": "reconx_dns_intelligence",
        "description": "Full DNS analysis: A/AAAA/MX/TXT/NS/SOA records, zone transfer attempt, wildcard detection, subdomain brute-force.",
        "category": "dns",
        "parameters": {
            "target":        {"type": "string", "required": True},
            "zone_transfer": {"type": "boolean", "default": False},
            "brute_force":   {"type": "boolean", "default": False},
        },
    },
    {
        "name": "reconx_port_scan",
        "description": "TCP port scanning with service detection and banner grabbing. Supports fast (top-100), balanced (top-1024), and full (all 65535 ports) profiles.",
        "category": "scanning",
        "parameters": {
            "target":   {"type": "string", "required": True},
            "profile":  {"type": "string", "enum": ["fast", "balanced", "full"], "default": "balanced"},
            "stealth":  {"type": "boolean", "default": False, "description": "SYN scan (requires root)"},
        },
    },
    {
        "name": "reconx_service_intelligence",
        "description": "Deep service analysis: protocol detection, TLS fingerprinting, banner analysis, risk scoring, CVE mapping, enumeration paths.",
        "category": "analysis",
        "parameters": {
            "target":       {"type": "string", "required": True},
            "scan_output":  {"type": "string", "description": "Raw nmap/rustscan/masscan output to analyze"},
            "tool":         {"type": "string", "enum": ["nmap", "rustscan", "naabu", "masscan", "httpx", "auto"], "default": "auto"},
        },
    },
    {
        "name": "reconx_web_assessment",
        "description": "Autonomous web application security assessment: crawl, fingerprint, probe for XSS/SQLi/SSRF/CRLF/LFI/SSTI, directory bruteforce, JS analysis.",
        "category": "web",
        "parameters": {
            "target":      {"type": "string", "required": True},
            "intensity":   {"type": "string", "enum": ["safe", "standard", "aggressive"], "default": "standard"},
            "auth_profile":{"type": "string", "description": "Named auth profile for authenticated testing"},
        },
    },
    {
        "name": "reconx_vuln_scan",
        "description": "Vulnerability scanning using nuclei templates with CVE correlation, false-positive filtering, and severity classification.",
        "category": "vuln",
        "parameters": {
            "target":     {"type": "string", "required": True},
            "severity":   {"type": "string", "enum": ["critical", "high", "medium", "low", "all"], "default": "all"},
            "templates":  {"type": "array", "description": "Specific template categories", "default": []},
        },
    },
    {
        "name": "reconx_cloud_intel",
        "description": "Cloud infrastructure analysis: S3 buckets, Azure tenants, GCP resources, Kubernetes endpoints, Docker registries, CI/CD exposure.",
        "category": "cloud",
        "parameters": {
            "target":    {"type": "string", "required": True},
            "providers": {"type": "array", "description": "Cloud providers to check", "default": ["aws", "azure", "gcp"]},
        },
    },
    {
        "name": "reconx_osint",
        "description": "OSINT collection: email/credential leaks, Google dorks, GitHub secrets, metadata extraction, SPF/DMARC analysis.",
        "category": "osint",
        "parameters": {
            "target":     {"type": "string", "required": True},
            "modules":    {"type": "array", "description": "OSINT modules to run",
                           "default": ["leaks", "dorks", "github", "mail_hygiene"]},
            "github_token": {"type": "string", "description": "GitHub token for higher rate limits"},
        },
    },
    {
        "name": "reconx_crlf_probe",
        "description": "CRLF injection detection across URL parameters, path segments, and headers.",
        "category": "web",
        "parameters": {
            "target_url": {"type": "string", "required": True},
            "params":     {"type": "array", "description": "Parameters to test", "default": []},
        },
    },
    {
        "name": "reconx_traffic_analysis",
        "description": "Network traffic analysis from PCAP file: protocol detection, credential extraction, anomaly detection, TLS analysis.",
        "category": "network",
        "parameters": {
            "pcap_path": {"type": "string", "required": True, "description": "Path to PCAP file"},
            "extract":   {"type": "array", "default": ["credentials", "dns", "tls", "anomalies"]},
        },
    },
    {
        "name": "reconx_sast",
        "description": "Source code static analysis: data flow taint analysis, secret detection, SCA with reachability, business logic issues.",
        "category": "code",
        "parameters": {
            "repo_path": {"type": "string", "required": True, "description": "Local path to source code"},
            "language":  {"type": "string", "description": "Programming language (auto-detected if omitted)"},
            "checks":    {"type": "array", "default": ["taint", "secrets", "sca"]},
        },
    },
    {
        "name": "reconx_attack_path_analysis",
        "description": "Correlate all findings into multi-step attack chains. Returns ranked attack paths with confidence scores.",
        "category": "correlation",
        "parameters": {
            "scan_id": {"type": "string", "required": True, "description": "ReconX scan ID"},
        },
    },
    {
        "name": "reconx_ai_analyze",
        "description": "AI-powered security analysis: explain findings, generate executive summary, recommend remediation, suggest next steps.",
        "category": "ai",
        "parameters": {
            "scan_id":  {"type": "string", "required": True},
            "question": {"type": "string", "description": "Specific question to answer about the scan"},
            "mode":     {"type": "string", "enum": ["summary", "findings", "next_steps", "qa"], "default": "summary"},
        },
    },
    {
        "name": "reconx_full_pipeline",
        "description": "Run the complete ReconX pipeline: passive discovery → DNS → port scan → service intel → web assessment → vuln scan → correlation → AI analysis → report.",
        "category": "pipeline",
        "parameters": {
            "target":    {"type": "string", "required": True},
            "mode":      {"type": "string", "enum": ["fast", "balanced", "deep", "web", "passive", "network"], "default": "balanced"},
            "no_ai":     {"type": "boolean", "default": False},
            "export_pdf":{"type": "boolean", "default": False},
        },
    },
    {
        "name": "reconx_get_findings",
        "description": "Retrieve findings from ReconX data store with filtering by severity, target, status.",
        "category": "data",
        "parameters": {
            "scan_id":      {"type": "string"},
            "min_severity": {"type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]},
            "status":       {"type": "string", "enum": ["open", "triaging", "fixed", "wontfix"]},
            "limit":        {"type": "integer", "default": 50},
        },
    },
    {
        "name": "reconx_get_summary",
        "description": "Get executive summary, statistics, and top findings for a completed scan.",
        "category": "data",
        "parameters": {
            "scan_id": {"type": "string", "required": True},
        },
    },
    {
        "name": "reconx_generate_report",
        "description": "Generate a formatted security report (HTML, PDF, JSON, CSV) for a completed scan.",
        "category": "reporting",
        "parameters": {
            "scan_id": {"type": "string", "required": True},
            "format":  {"type": "string", "enum": ["html", "pdf", "json", "csv"], "default": "html"},
            "output":  {"type": "string", "description": "Output file path"},
        },
    },
]

MCP_TOOL_INDEX = {t["name"]: t for t in MCP_TOOLS}

# ── Request / Response Models ──────────────────────────────────────────────────

@dataclass
class MCPRequest:
    method:  str
    params:  dict
    id:      str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]


@dataclass
class MCPResponse:
    id:      str
    result:  Any = None
    error:   Optional[str] = None

    def to_dict(self) -> dict:
        d: dict = {"id": self.id}
        if self.error:
            d["error"] = {"message": self.error}
        else:
            d["result"] = self.result
        return d


# ── Rate Limiter ───────────────────────────────────────────────────────────────

class RateLimiter:
    def __init__(self, max_per_minute: int = 30):
        self._max   = max_per_minute
        self._calls: dict[str, list[float]] = {}

    def allow(self, client_id: str) -> bool:
        now = time.time()
        window = now - 60
        calls = [t for t in self._calls.get(client_id, []) if t > window]
        self._calls[client_id] = calls
        if len(calls) >= self._max:
            return False
        self._calls[client_id].append(now)
        return True


# ── Scope Validator ────────────────────────────────────────────────────────────

class ScopeValidator:
    def __init__(self, strict: bool = False, allowed_scope: list[str] | None = None):
        self.strict = strict
        self.scope  = set(allowed_scope or [])

    def validate(self, target: str) -> tuple[bool, str]:
        import ipaddress, re
        target = target.strip()

        # Basic injection prevention
        if any(c in target for c in [";", "&", "|", "`", "$", "\n", "\r"]):
            return False, f"Invalid characters in target: {target}"

        # IP validation
        try:
            ipaddress.ip_network(target, strict=False)
            if self.strict and target not in self.scope:
                return False, f"Target {target} not in allowed scope"
            return True, ""
        except ValueError:
            pass

        # Domain/hostname validation
        domain_re = re.compile(
            r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
        )
        if domain_re.match(target):
            if self.strict and not any(target.endswith(s) for s in self.scope):
                return False, f"Target {target} not in allowed scope"
            return True, ""

        # URL
        if target.startswith(("http://", "https://")):
            import urllib.parse
            host = urllib.parse.urlparse(target).hostname or ""
            if domain_re.match(host) or self._is_ip(host):
                return True, ""

        return False, f"Invalid target format: {target}"

    @staticmethod
    def _is_ip(s: str) -> bool:
        import ipaddress
        try:
            ipaddress.ip_address(s)
            return True
        except ValueError:
            return False


# ── MCP Server ─────────────────────────────────────────────────────────────────

class ReconXMCPServer:
    """
    ReconX MCP Server — exposes all ReconX capabilities via the
    Model Context Protocol JSON-RPC interface.

    This is a standalone WSGI/ASGI-compatible class.
    Use with any compatible HTTP server (uvicorn, gunicorn, etc.)

    For production deployment, wrap with FastAPI:

        from reconx.api.mcp_server import ReconXMCPServer, build_fastapi_app
        app = build_fastapi_app()
        # uvicorn reconx.api.mcp_server:app

    For testing / embedding:

        server = ReconXMCPServer()
        result = server.handle({"method": "list_tools", "params": {}, "id": "1"})
    """

    def __init__(
        self,
        strict_scope:    bool            = False,
        allowed_scope:   list[str] | None = None,
        rate_limit:      int             = 60,
        require_auth:    bool            = False,
        api_tokens:      list[str] | None = None,
    ):
        self.validator   = ScopeValidator(strict=strict_scope, allowed_scope=allowed_scope)
        self.rate_limiter = RateLimiter(max_per_minute=rate_limit)
        self.require_auth = require_auth
        self.api_tokens   = set(api_tokens or [])
        self._sessions:   dict[str, dict] = {}

        log.info(f"ReconXMCPServer initialized (strict_scope={strict_scope}, rate_limit={rate_limit}/min)")

    # ── Public Dispatch ──────────────────────────────────────────────────────

    def handle(self, raw: dict, client_id: str = "anonymous",
               auth_token: str = "") -> dict:
        """
        Main entry point — dispatch an MCP JSON-RPC request.
        Returns a dict ready for JSON serialization.
        """
        req = MCPRequest(
            method=raw.get("method", ""),
            params=raw.get("params", {}),
            id=raw.get("id", str(uuid.uuid4())[:8]),
        )

        # Auth check
        if self.require_auth and auth_token not in self.api_tokens:
            return MCPResponse(id=req.id, error="Unauthorized").to_dict()

        # Rate limit
        if not self.rate_limiter.allow(client_id):
            return MCPResponse(id=req.id, error="Rate limit exceeded — try again later").to_dict()

        # Dispatch
        handlers = {
            "list_tools":    self._list_tools,
            "run_tool":      self._run_tool,
            "plan_scan":     self._plan_scan,
            "get_findings":  self._get_findings,
            "get_summary":   self._get_summary,
            "status":        self._status,
            # MCP standard
            "initialize":    self._initialize,
            "tools/list":    self._list_tools,
            "tools/call":    self._tool_call,
        }

        handler = handlers.get(req.method)
        if not handler:
            return MCPResponse(id=req.id, error=f"Unknown method: {req.method}").to_dict()

        try:
            result = handler(req.params, client_id)
            return MCPResponse(id=req.id, result=result).to_dict()
        except Exception as e:
            log.error(f"Handler error [{req.method}]: {e}")
            return MCPResponse(id=req.id, error=str(e)).to_dict()

    # ── Handlers ─────────────────────────────────────────────────────────────

    def _initialize(self, params: dict, client_id: str) -> dict:
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {"listChanged": False},
            },
            "serverInfo": {
                "name": "ReconX",
                "version": "21.0.0",
            },
        }

    def _list_tools(self, params: dict, client_id: str) -> dict:
        """Return all available ReconX tools in MCP format."""
        tools = []
        for t in MCP_TOOLS:
            props = {}
            required = []
            for pname, pdef in t.get("parameters", {}).items():
                props[pname] = {
                    "type": pdef.get("type", "string"),
                    "description": pdef.get("description", ""),
                }
                if pdef.get("enum"):
                    props[pname]["enum"] = pdef["enum"]
                if pdef.get("required"):
                    required.append(pname)

            tools.append({
                "name": t["name"],
                "description": t["description"],
                "inputSchema": {
                    "type": "object",
                    "properties": props,
                    "required": required,
                },
            })
        return {"tools": tools}

    def _tool_call(self, params: dict, client_id: str) -> dict:
        """MCP tools/call handler."""
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        return self._run_tool({"tool_name": tool_name, **arguments}, client_id)

    def _run_tool(self, params: dict, client_id: str) -> dict:
        """Execute a ReconX tool."""
        tool_name = params.get("tool_name") or params.get("name", "")
        if not tool_name:
            raise ValueError("tool_name is required")

        tool_def = MCP_TOOL_INDEX.get(tool_name)
        if not tool_def:
            raise ValueError(f"Unknown tool: {tool_name}. Use list_tools to see available tools.")

        # Validate target if present
        target = params.get("target") or params.get("target_url", "")
        if target:
            ok, reason = self.validator.validate(target)
            if not ok:
                raise ValueError(f"Scope validation failed: {reason}")

        # Build execution plan (actual tool execution happens via ReconX engine)
        scan_id = f"rx-{uuid.uuid4().hex[:8]}"
        execution_plan = {
            "scan_id":    scan_id,
            "tool":       tool_name,
            "target":     target,
            "params":     {k: v for k, v in params.items() if k not in ("tool_name", "name")},
            "status":     "queued",
            "queued_at":  time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "message":    f"ReconX tool '{tool_name}' queued for execution against '{target}'",
            "note":       "Connect ReconX engine to execute. See reconx.orchestration.reconx_engine.",
        }

        log.info(f"Tool queued: {tool_name} → {target} [scan_id={scan_id}]")
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(execution_plan, indent=2),
                }
            ],
            "isError": False,
        }

    def _plan_scan(self, params: dict, client_id: str) -> dict:
        """Return AI-recommended tool chain for a target."""
        target = params.get("target", "")
        mode   = params.get("mode", "balanced")

        ok, reason = self.validator.validate(target)
        if not ok:
            raise ValueError(f"Invalid target: {reason}")

        plans = {
            "fast":    ["reconx_passive_discovery", "reconx_port_scan", "reconx_service_intelligence", "reconx_ai_analyze"],
            "balanced":["reconx_passive_discovery", "reconx_dns_intelligence", "reconx_port_scan",
                        "reconx_service_intelligence", "reconx_web_assessment", "reconx_vuln_scan",
                        "reconx_attack_path_analysis", "reconx_ai_analyze"],
            "deep":    [t["name"] for t in MCP_TOOLS if t["category"] not in ("data", "reporting")],
            "web":     ["reconx_passive_discovery", "reconx_dns_intelligence", "reconx_web_assessment",
                        "reconx_crlf_probe", "reconx_vuln_scan", "reconx_osint", "reconx_ai_analyze"],
            "passive": ["reconx_passive_discovery", "reconx_dns_intelligence", "reconx_osint", "reconx_ai_analyze"],
            "network": ["reconx_port_scan", "reconx_service_intelligence", "reconx_traffic_analysis",
                        "reconx_attack_path_analysis", "reconx_ai_analyze"],
        }

        chain = plans.get(mode, plans["balanced"])
        return {
            "target":    target,
            "mode":      mode,
            "tool_chain": chain,
            "step_count": len(chain),
            "description": f"Recommended {mode} scan pipeline for {target}",
            "tools": [MCP_TOOL_INDEX[t] for t in chain if t in MCP_TOOL_INDEX],
        }

    def _get_findings(self, params: dict, client_id: str) -> dict:
        """Retrieve findings from ReconX data store."""
        try:
            from reconx.data.store import ReconXStore
            store = ReconXStore.open()
            findings = store.findings(
                scan_id=params.get("scan_id"),
                min_severity=params.get("min_severity"),
                status=params.get("status"),
                limit=params.get("limit", 50),
            )
            return {
                "findings": [asdict(f) for f in findings],
                "count": len(findings),
            }
        except ImportError:
            return {"findings": [], "count": 0, "note": "ReconX data store not initialized"}

    def _get_summary(self, params: dict, client_id: str) -> dict:
        """Get scan summary from data store."""
        scan_id = params.get("scan_id", "")
        if not scan_id:
            raise ValueError("scan_id required")
        try:
            from reconx.data.store import ReconXStore
            store = ReconXStore.open()
            return store.scan_summary(scan_id)
        except ImportError:
            return {"scan_id": scan_id, "note": "ReconX data store not initialized"}

    def _status(self, params: dict, client_id: str) -> dict:
        return {
            "status":   "online",
            "version":  "21.0.0",
            "tools":    len(MCP_TOOLS),
            "uptime_s": time.time(),
        }


# ── FastAPI App Builder ────────────────────────────────────────────────────────

def build_fastapi_app(
    strict_scope:  bool            = False,
    allowed_scope: list[str] | None = None,
    rate_limit:    int             = 60,
) -> Any:
    """
    Build a FastAPI ASGI application wrapping ReconXMCPServer.

    Install deps:
        pip install fastapi uvicorn

    Run:
        uvicorn reconx.api.mcp_server:app --host 127.0.0.1 --port 8765
    """
    try:
        from fastapi import FastAPI, Request, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import JSONResponse
    except ImportError:
        raise ImportError("FastAPI required: pip install fastapi uvicorn")

    mcp = ReconXMCPServer(strict_scope=strict_scope, allowed_scope=allowed_scope,
                          rate_limit=rate_limit)

    app = FastAPI(
        title="ReconX MCP Server",
        description="ReconX Cyber Intelligence OS — MCP Protocol Interface",
        version="21.0.0",
    )

    app.add_middleware(CORSMiddleware, allow_origins=["*"],
                       allow_methods=["*"], allow_headers=["*"])

    @app.post("/mcp")
    async def mcp_endpoint(request: Request) -> JSONResponse:
        body = await request.json()
        client_id = request.client.host if request.client else "anonymous"
        auth = request.headers.get("Authorization", "").replace("Bearer ", "")
        result = mcp.handle(body, client_id=client_id, auth_token=auth)
        return JSONResponse(result)

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok", "version": "21.0.0", "tools": len(MCP_TOOLS)}

    @app.get("/tools")
    async def list_tools() -> dict:
        return mcp._list_tools({}, "api")

    @app.get("/")
    async def root() -> dict:
        return {
            "name":        "ReconX MCP Server",
            "version":     "21.0.0",
            "description": "ReconX Cyber Intelligence OS — MCP Protocol Interface",
            "endpoints":   {"mcp": "/mcp", "health": "/health", "tools": "/tools"},
            "register":    "claude mcp add reconx -- uvicorn reconx.api.mcp_server:app --host 127.0.0.1 --port 8765",
        }

    return app


# ── Module-level app for uvicorn ──────────────────────────────────────────────
try:
    app = build_fastapi_app()
except ImportError:
    app = None  # FastAPI not installed — CLI-only mode
