"""
ReconX — Agentic Analysis Loop
================================
Absorbed from METATRON/llm.py — full working implementation.

The agentic loop lets the LLM drive its own tool execution:
  - LLM can write [TOOL: nmap -sV 10.0.0.1] in its response
  - LLM can write [SEARCH: CVE-2021-44228 exploit] in its response
  - ReconX executes the tool/search and feeds results back
  - Loop continues until analysis is complete or MAX_ROUNDS reached

Key components:
  AgenticLoop          — main loop orchestrator
  ToolCallExtractor    — parses [TOOL:] and [SEARCH:] tags from LLM text
  OutputCompressor     — shrinks long tool outputs for LLM context
  VulnerabilityParser  — extracts VULN:/SEVERITY:/PORT: structured data
  ExploitParser        — extracts EXPLOIT:/TOOL:/PAYLOAD: structured data
  RiskParser           — extracts RISK_LEVEL: / SUMMARY: from response
  SafeToolRunner       — runs only allowlisted commands
"""
from __future__ import annotations

import logging
import re
import shlex
import subprocess
import time
from dataclasses import dataclass, field
from typing import Optional

from .intelligence_search import handle_search_dispatch

log = logging.getLogger("reconx.ai.agentic_loop")

# ── Safety: only these tool binaries may be called ───────────────────────────

ALLOWED_TOOLS = frozenset([
    "nmap", "rustscan", "masscan", "naabu",
    "whois", "dig", "host", "nslookup",
    "curl", "wget", "httpx",
    "whatweb", "wafw00f",
    "nikto",
    "gobuster", "ffuf", "feroxbuster", "dirsearch",
    "nuclei",
    "subfinder", "assetfinder", "amass",
    "dnsx", "massdns", "puredns", "shuffledns",
    "enum4linux", "enum4linux-ng",
    "smbclient", "rpcclient", "crackmapexec",
    "ldapsearch",
    "openssl", "sslyze", "testssl.sh",
    "sqlmap", "dalfox",
    "gitleaks", "trufflehog",
    "aws", "gcloud", "az",
    "python3", "python",  # for safe one-liners only
])

MAX_TOOL_ROUNDS = 9      # Maximum LLM→tool iterations per analysis
MAX_OUTPUT_LEN  = 6000   # Characters before compressing tool output
COMPRESS_TARGET = 500    # Characters after compression


# ── Data models ───────────────────────────────────────────────────────────────

@dataclass
class ToolCall:
    kind:    str    # "TOOL" | "SEARCH"
    content: str    # the command string or search query


@dataclass
class ParsedVuln:
    vuln_name:   str
    severity:    str
    port:        str
    service:     str
    description: str
    fix:         str


@dataclass
class ParsedExploit:
    exploit_name: str
    tool_used:    str
    payload:      str
    result:       str
    notes:        str


@dataclass
class AgenticResult:
    target:          str
    full_response:   str
    vulnerabilities: list[ParsedVuln]   = field(default_factory=list)
    exploits:        list[ParsedExploit] = field(default_factory=list)
    risk_level:      str                = "UNKNOWN"
    summary:         str                = ""
    raw_scan:        str                = ""
    rounds:          int                = 0
    tool_calls_made: list[str]          = field(default_factory=list)


# ── Tool Call Extractor ───────────────────────────────────────────────────────

_TOOL_RE   = re.compile(r"\[TOOL:\s*(.+?)\]",   re.DOTALL)
_SEARCH_RE = re.compile(r"\[SEARCH:\s*(.+?)\]", re.DOTALL)


def extract_tool_calls(response: str) -> list[ToolCall]:
    """
    Extract all [TOOL: ...] and [SEARCH: ...] tags from LLM response.
    Returns list of ToolCall objects in order of appearance.
    """
    calls: list[ToolCall] = []
    for m in _TOOL_RE.finditer(response):
        calls.append(ToolCall(kind="TOOL", content=m.group(1).strip()))
    for m in _SEARCH_RE.finditer(response):
        calls.append(ToolCall(kind="SEARCH", content=m.group(1).strip()))
    return calls


# ── Safe Tool Runner ──────────────────────────────────────────────────────────

class SafeToolRunner:
    """
    Executes shell commands with strict allowlisting.
    Prevents injection via argument sanitization.
    """

    def __init__(self, timeout: int = 120):
        self.timeout = timeout

    def run(self, command_str: str) -> str:
        """
        Parse and execute a command string safely.
        Returns combined stdout+stderr as string.
        """
        try:
            parts = shlex.split(command_str.strip())
        except ValueError as e:
            return f"[!] Invalid command syntax: {e}"

        if not parts:
            return "[!] Empty command."

        binary = parts[0].split("/")[-1].lower()   # strip path components
        if binary not in ALLOWED_TOOLS:
            return (f"[!] Tool '{parts[0]}' is not in the ReconX allowlist.\n"
                    f"    Allowed: {', '.join(sorted(ALLOWED_TOOLS))}")

        # Reject shell metacharacters in any argument
        for arg in parts[1:]:
            if any(c in arg for c in (";", "|", "&", "`", "$", "\n", "\r", ">")):
                return f"[!] Rejected: argument contains unsafe characters: {arg!r}"

        log.info("SafeToolRunner: %s", " ".join(parts[:6]))
        try:
            result = subprocess.run(
                parts,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            if stdout and stderr:
                return stdout + "\n[STDERR]\n" + stderr
            return stdout or stderr or "[!] Tool returned no output."
        except subprocess.TimeoutExpired:
            return f"[!] Timed out after {self.timeout}s: {command_str[:60]}"
        except FileNotFoundError:
            return f"[!] Not found: {parts[0]} — install it first."
        except Exception as e:
            return f"[!] Execution error: {e}"


# ── Output Compressor ─────────────────────────────────────────────────────────

class OutputCompressor:
    """
    Compresses long tool output for LLM context management.

    When tool output exceeds MAX_OUTPUT_LEN characters, this extracts
    security-relevant lines and truncates intelligently — preserving
    findings while reducing token cost.
    """

    # Lines containing these keywords are always preserved
    SECURITY_KEYWORDS = (
        "open", "filtered", "closed",
        "vuln", "cve", "exploit", "critical", "high", "medium",
        "warning", "error", "failed", "success",
        "ssh", "http", "https", "ftp", "smb", "rdp",
        "password", "credential", "auth", "token", "key", "secret",
        "admin", "root", "shell",
        "found", "discovered", "detected",
        "version", "service", "port",
        "VULN:", "SEVERITY:", "PORT:", "SERVICE:",
    )

    def __init__(self, llm=None):
        self._llm = llm   # Optional LLMAdapter for AI-assisted compression

    def compress(self, raw_output: str, source: str = "") -> str:
        """
        Compress raw tool output.

        If an LLM is available, uses it for intelligent summarization.
        Otherwise falls back to keyword-based line extraction.
        """
        if len(raw_output) <= MAX_OUTPUT_LEN:
            return raw_output

        log.debug("Compressing %d chars from %s", len(raw_output), source or "tool")

        if self._llm:
            return self._llm_compress(raw_output, source)
        return self._keyword_compress(raw_output)

    def _llm_compress(self, raw: str, source: str) -> str:
        """Use LLM to summarize tool output into security-relevant bullets."""
        prompt = (
            f"Compress this security tool output into maximum 15 bullet points.\n"
            f"Keep only security-relevant facts: open ports, versions, vulns, "
            f"credentials, CVEs, misconfigs.\n"
            f"Plain text only. No markdown headers.\n\n"
            f"Tool output from {source}:\n{raw[:MAX_OUTPUT_LEN]}"
        )
        try:
            resp = self._llm.ask(prompt, max_tokens=400)
            if resp.ok:
                return resp.text
        except Exception:
            pass
        return self._keyword_compress(raw)

    def _keyword_compress(self, raw: str) -> str:
        """Keyword-based extraction fallback."""
        lines = raw.splitlines()
        kept: list[str] = []
        kw_lower = [kw.lower() for kw in self.SECURITY_KEYWORDS]

        for line in lines:
            ll = line.lower()
            if any(kw in ll for kw in kw_lower):
                kept.append(line.strip())

        if not kept:
            # Nothing matched — return first + last portions
            head = "\n".join(lines[:20])
            tail = "\n".join(lines[-10:]) if len(lines) > 30 else ""
            return head + ("\n...\n" + tail if tail else "")

        result = "\n".join(kept[:60])
        if len(result) > COMPRESS_TARGET * 3:
            result = result[:COMPRESS_TARGET * 3] + "\n... [further truncated]"
        return result


# ── Structured Parsers ────────────────────────────────────────────────────────

_CLEAN_RE = re.compile(r"\*+")


def _clean(line: str) -> str:
    """Strip markdown bold markers."""
    return _CLEAN_RE.sub("", line).strip()


def parse_vulnerabilities(response: str) -> list[ParsedVuln]:
    """
    Extract VULN: structured blocks from LLM response.

    Expected format (from system prompt):
        VULN: <name> | SEVERITY: <level> | PORT: <port> | SERVICE: <service>
        DESC: <description>
        FIX: <fix recommendation>
    """
    vulns: list[ParsedVuln] = []
    lines = response.splitlines()
    i = 0
    while i < len(lines):
        line = _clean(lines[i])
        if not line.upper().startswith("VULN:"):
            i += 1
            continue

        vuln = ParsedVuln(vuln_name="", severity="medium", port="", service="",
                          description="", fix="")

        for part in line.split("|"):
            part = part.strip()
            if part.upper().startswith("VULN:"):
                vuln.vuln_name = part[5:].strip()
            elif part.upper().startswith("SEVERITY:"):
                vuln.severity = part[9:].strip().lower()
            elif part.upper().startswith("PORT:"):
                vuln.port = part[5:].strip()
            elif part.upper().startswith("SERVICE:"):
                vuln.service = part[8:].strip()

        # Look ahead for DESC: and FIX:
        j = i + 1
        while j < len(lines) and j <= i + 6:
            next_line = _clean(lines[j])
            upper = next_line.upper()
            if upper.startswith(("VULN:", "EXPLOIT:", "RISK_LEVEL:", "SUMMARY:")):
                break
            if upper.startswith("DESC:"):
                vuln.description = next_line[5:].strip()
            elif upper.startswith("FIX:"):
                vuln.fix = next_line[4:].strip()
            j += 1

        if vuln.vuln_name:
            vulns.append(vuln)
        i = j
    return vulns


def parse_exploits(response: str) -> list[ParsedExploit]:
    """
    Extract EXPLOIT: structured blocks from LLM response.

    Expected format:
        EXPLOIT: <name> | TOOL: <tool> | PAYLOAD: <payload>
        RESULT: <expected result>
        NOTES: <notes>
    """
    exploits: list[ParsedExploit] = []
    lines = response.splitlines()
    i = 0
    while i < len(lines):
        line = _clean(lines[i])
        if not line.upper().startswith("EXPLOIT:"):
            i += 1
            continue

        exploit = ParsedExploit(exploit_name="", tool_used="", payload="",
                                result="unknown", notes="")

        for part in line.split("|"):
            part = part.strip()
            if part.upper().startswith("EXPLOIT:"):
                exploit.exploit_name = part[8:].strip()
            elif part.upper().startswith("TOOL:"):
                exploit.tool_used = part[5:].strip()
            elif part.upper().startswith("PAYLOAD:"):
                exploit.payload = part[8:].strip()

        j = i + 1
        while j < len(lines) and j <= i + 5:
            next_line = _clean(lines[j])
            upper = next_line.upper()
            if upper.startswith(("VULN:", "EXPLOIT:", "RISK_LEVEL:", "SUMMARY:")):
                break
            if upper.startswith("RESULT:"):
                exploit.result = next_line[7:].strip()
            elif upper.startswith("NOTES:"):
                exploit.notes = next_line[6:].strip()
            j += 1

        if exploit.exploit_name:
            exploits.append(exploit)
        i = j
    return exploits


_RISK_RE    = re.compile(r"RISK_LEVEL:\s*(CRITICAL|HIGH|MEDIUM|LOW)", re.IGNORECASE)
_SUMMARY_RE = re.compile(r"SUMMARY:\s*(.+)",                          re.IGNORECASE)


def parse_risk_level(response: str) -> str:
    m = _RISK_RE.search(response)
    return m.group(1).upper() if m else "UNKNOWN"


def parse_summary(response: str) -> str:
    m = _SUMMARY_RE.search(response)
    return m.group(1).strip() if m else ""


# ── Agentic Loop ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are the ReconX AI Security Analyst — an embedded expert cybersecurity assistant.

You have access to real tools. To use them, write tags in your response:
  [TOOL: nmap -sV 192.168.1.1]          → runs nmap or any allowed CLI tool
  [SEARCH: CVE-2021-44228 exploit]      → searches the web via DuckDuckGo

RULES:
- Analyze scan data thoroughly before suggesting further investigation
- List vulnerabilities in this EXACT format:
  VULN: <name> | SEVERITY: <critical|high|medium|low> | PORT: <port> | SERVICE: <service>
  DESC: <description>
  FIX: <fix recommendation>

- List exploits in this EXACT format:
  EXPLOIT: <name> | TOOL: <tool> | PAYLOAD: <payload or description>
  RESULT: <expected result>
  NOTES: <any notes>

- End your analysis with:
  RISK_LEVEL: <CRITICAL|HIGH|MEDIUM|LOW>
  SUMMARY: <2-3 sentence overall summary>

ACCURACY RULES:
- nmap 'filtered' means INCONCLUSIVE, not vulnerable
- Never assert a version without seeing it in scan output
- Never infer CVEs from guessed versions — only from confirmed banners
- curl timeouts and HTTP 000 mean the host is unreachable, not exploitable
- Only assign CRITICAL if there is direct evidence of exploitability
- If evidence is weak, mark severity as LOW with note: unconfirmed

Plain text only. No markdown bold (**) or headers (##)."""


class AgenticLoop:
    """
    Multi-round agentic analysis loop.

    Each round:
      1. Send context + scan data to LLM
      2. LLM responds with analysis + optional [TOOL:]/[SEARCH:] tags
      3. Execute tagged tools/searches
      4. Feed results back to LLM as next-round context
      5. Repeat until no more tool calls or MAX_TOOL_ROUNDS reached

    Absorbed from METATRON/llm.py — analyse_target() + full loop.
    """

    def __init__(
        self,
        llm,                           # LLMAdapter instance
        tool_runner: Optional[SafeToolRunner]   = None,
        compressor:  Optional[OutputCompressor] = None,
        max_rounds:  int = MAX_TOOL_ROUNDS,
    ):
        self._llm        = llm
        self._runner     = tool_runner or SafeToolRunner()
        self._compressor = compressor  or OutputCompressor(llm=llm)
        self._max_rounds = max_rounds

    def analyse(self, target: str, raw_scan: str) -> AgenticResult:
        """
        Run the full agentic analysis loop for a target.

        Args:
            target:   IP, hostname, or URL
            raw_scan: Pre-collected scan data (nmap output, whois, etc.)

        Returns:
            AgenticResult with structured vulnerabilities, exploits, risk level
        """
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": self._initial_prompt(target, raw_scan)},
        ]

        final_response  = ""
        all_tool_calls  = []

        for round_num in range(1, self._max_rounds + 1):
            log.info("[Agentic round %d/%d] target=%s", round_num, self._max_rounds, target)

            # Ask LLM
            response = self._llm.ask(
                prompt=messages[-1]["content"],
                system=SYSTEM_PROMPT if len(messages) == 1 else "",
                max_tokens=2000,
            )

            if not response.ok:
                log.warning("LLM response error: %s", response.error)
                break

            text = response.text
            final_response = text

            # Extract tool calls
            calls = extract_tool_calls(text)
            if not calls:
                log.info("[Agentic] No tool calls in round %d — complete", round_num)
                break

            # Execute all tool calls, compress output
            tool_results = ""
            for call in calls:
                all_tool_calls.append(f"{call.kind}: {call.content[:60]}")
                log.info("  [%s] %s", call.kind, call.content[:80])

                if call.kind == "TOOL":
                    raw_out = self._runner.run(call.content)
                elif call.kind == "SEARCH":
                    raw_out = handle_search_dispatch(call.content)
                else:
                    raw_out = f"[!] Unknown call type: {call.kind}"

                compressed = self._compressor.compress(raw_out, source=call.content[:30])
                tool_results += f"\n[{call.kind} RESULT: {call.content[:60]}]\n"
                tool_results += "─" * 40 + "\n"
                tool_results += compressed + "\n"

            # Add assistant turn + tool results as next user message
            messages.append({"role": "assistant", "content": text})
            messages.append({
                "role": "user",
                "content": (
                    f"[TOOL RESULTS — round {round_num}]\n"
                    f"{tool_results}\n\n"
                    "Continue your analysis with this new information.\n"
                    "If analysis is complete, provide the final RISK_LEVEL and SUMMARY.\n"
                    "If you need more information, use [TOOL:] or [SEARCH:] again."
                ),
            })

        # Parse structured data from final response
        return AgenticResult(
            target=target,
            full_response=final_response,
            vulnerabilities=parse_vulnerabilities(final_response),
            exploits=parse_exploits(final_response),
            risk_level=parse_risk_level(final_response),
            summary=parse_summary(final_response),
            raw_scan=raw_scan,
            rounds=min(round_num, self._max_rounds),  # type: ignore[name-defined]
            tool_calls_made=all_tool_calls,
        )

    @staticmethod
    def _initial_prompt(target: str, raw_scan: str) -> str:
        return (
            f"TARGET: {target}\n\n"
            f"RECON DATA:\n{raw_scan}\n\n"
            "Analyze this target completely.\n"
            "Use [TOOL:] or [SEARCH:] if you need additional information.\n"
            "List all vulnerabilities, fixes, and suggest exploits where confirmed.\n"
            "End with RISK_LEVEL: and SUMMARY:"
        )


# ── Convenience function ──────────────────────────────────────────────────────

def analyse_target(target: str, raw_scan: str, llm=None) -> AgenticResult:
    """
    Top-level convenience function matching METATRON's analyse_target() API.

    Usage:
        from reconx.ai.agentic_loop import analyse_target
        from reconx.ai.llm_adapter import LLMAdapter
        adapter = LLMAdapter.auto()
        result  = analyse_target("192.168.1.1", nmap_output, llm=adapter)
        print(result.risk_level)
        for v in result.vulnerabilities:
            print(v.severity, v.vuln_name)
    """
    if llm is None:
        try:
            from .llm_adapter import LLMAdapter
            llm = LLMAdapter.auto()
        except Exception:
            raise ValueError("llm parameter required or LLMAdapter must be importable")

    loop = AgenticLoop(llm=llm)
    return loop.analyse(target, raw_scan)
