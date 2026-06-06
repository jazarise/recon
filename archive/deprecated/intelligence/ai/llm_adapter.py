"""
ReconX — Stage 21: Unified LLM Adapter
=======================================
Provides a single interface for all AI analysis in ReconX.
Supports:
  - Ollama (local, any model — llama3, mistral, qwen, etc.)
  - Anthropic Claude API (cloud)
  - Fallback: rule-based summary when no LLM is available

No module in ReconX should import Ollama or Claude directly.
All AI calls go through this adapter.

Usage:
    adapter = LLMAdapter.auto()           # auto-detect best available
    response = adapter.ask("Explain this Redis exposure...")
    response = adapter.analyze_findings(findings, context)
    response = adapter.generate_summary(report_data)
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

log = logging.getLogger("reconx.ai.llm_adapter")

# ── Response Model ─────────────────────────────────────────────────────────────

@dataclass
class LLMResponse:
    text:      str
    provider:  str              # "ollama" | "claude" | "rule-based"
    model:     str
    tokens:    int = 0
    latency_s: float = 0.0
    error:     Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.error is None and bool(self.text.strip())


# ── Base Provider ──────────────────────────────────────────────────────────────

class LLMProvider(ABC):
    name: str = "base"

    @abstractmethod
    def available(self) -> bool: ...

    @abstractmethod
    def ask(self, prompt: str, system: str = "", max_tokens: int = 1024) -> LLMResponse: ...

    def analyze_findings(self, findings: list[dict], context: dict) -> LLMResponse:
        prompt = _build_findings_prompt(findings, context)
        return self.ask(prompt, system=SECURITY_ANALYST_SYSTEM)

    def generate_summary(self, report_data: dict) -> LLMResponse:
        prompt = _build_summary_prompt(report_data)
        return self.ask(prompt, system=SECURITY_ANALYST_SYSTEM, max_tokens=2048)

    def explain_cve(self, cve: str, service: str, target_context: str) -> LLMResponse:
        prompt = (
            f"CVE: {cve}\nService: {service}\nContext: {target_context}\n\n"
            "Explain this CVE in plain English: what it is, who is at risk, "
            "what an attacker could do, and how to fix it. Be concise and structured."
        )
        return self.ask(prompt, system=SECURITY_ANALYST_SYSTEM)

    def recommend_next_steps(self, context: dict) -> LLMResponse:
        prompt = _build_next_steps_prompt(context)
        return self.ask(prompt, system=SECURITY_ANALYST_SYSTEM)


# ── Ollama Provider ────────────────────────────────────────────────────────────

class OllamaProvider(LLMProvider):
    name = "ollama"

    def __init__(self, model: str = "llama3", host: str = "http://localhost:11434"):
        self.model = model
        self.host  = host.rstrip("/")
        self._available: Optional[bool] = None

    def available(self) -> bool:
        if self._available is not None:
            return self._available
        try:
            import urllib.request
            with urllib.request.urlopen(f"{self.host}/api/tags", timeout=2) as r:
                data = json.loads(r.read())
                models = [m["name"] for m in data.get("models", [])]
                self._available = any(self.model in m for m in models)
        except Exception as e:
            log.debug(f"Ollama not available: {e}")
            self._available = False
        return self._available

    def ask(self, prompt: str, system: str = "", max_tokens: int = 1024) -> LLMResponse:
        import time, urllib.request, urllib.error
        t0 = time.time()
        try:
            payload = json.dumps({
                "model":  self.model,
                "prompt": prompt,
                "system": system,
                "stream": False,
                "options": {"num_predict": max_tokens},
            }).encode()
            req = urllib.request.Request(
                f"{self.host}/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read())
            text = data.get("response", "").strip()
            return LLMResponse(
                text=text, provider="ollama", model=self.model,
                tokens=data.get("eval_count", 0),
                latency_s=round(time.time()-t0, 2),
            )
        except Exception as e:
            return LLMResponse(text="", provider="ollama", model=self.model,
                               latency_s=round(time.time()-t0, 2), error=str(e))


# ── Claude API Provider ────────────────────────────────────────────────────────

class ClaudeProvider(LLMProvider):
    name = "claude"

    DEFAULT_MODEL = "claude-haiku-4-5-20251001"  # fast + affordable for analysis

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.model   = model or self.DEFAULT_MODEL

    def available(self) -> bool:
        return bool(self.api_key)

    def ask(self, prompt: str, system: str = "", max_tokens: int = 1024) -> LLMResponse:
        import time, urllib.request
        if not self.available():
            return LLMResponse(text="", provider="claude", model=self.model,
                               error="No ANTHROPIC_API_KEY configured")
        t0 = time.time()
        try:
            msgs = [{"role": "user", "content": prompt}]
            body: dict[str, Any] = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": msgs,
            }
            if system:
                body["system"] = system
            payload = json.dumps(body).encode()
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=payload,
                headers={
                    "Content-Type":      "application/json",
                    "x-api-key":         self.api_key,
                    "anthropic-version": "2023-06-01",
                },
            )
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read())
            text = data["content"][0]["text"].strip()
            usage = data.get("usage", {})
            return LLMResponse(
                text=text, provider="claude", model=self.model,
                tokens=usage.get("output_tokens", 0),
                latency_s=round(time.time()-t0, 2),
            )
        except Exception as e:
            return LLMResponse(text="", provider="claude", model=self.model,
                               latency_s=round(time.time()-t0, 2), error=str(e))


# ── Rule-Based Fallback ────────────────────────────────────────────────────────

class RuleBasedProvider(LLMProvider):
    """Always-available fallback that generates structured analysis without LLM."""
    name = "rule-based"

    def available(self) -> bool:
        return True

    def ask(self, prompt: str, system: str = "", max_tokens: int = 1024) -> LLMResponse:
        # Simple keyword-based response generation
        text = (
            "[ReconX Rule-Based Analysis — No LLM Available]\n\n"
            "Configure Ollama (local) or set ANTHROPIC_API_KEY for AI analysis.\n"
            "Static risk scoring and CVE correlation are still active.\n\n"
            "To enable AI:\n"
            "  1. Ollama: `ollama pull llama3 && ollama serve`\n"
            "  2. Claude:  export ANTHROPIC_API_KEY=sk-ant-...\n"
            "  3. Restart ReconX."
        )
        return LLMResponse(text=text, provider="rule-based", model="static")


# ── Adapter (public API) ───────────────────────────────────────────────────────

class LLMAdapter:
    """
    Unified LLM interface for ReconX.

    Priority order (configurable):
      1. Ollama (local — preferred for offline/privacy)
      2. Claude API (cloud — best quality)
      3. Rule-based fallback (always available)
    """

    def __init__(self, provider: LLMProvider):
        self._provider = provider
        log.info(f"LLMAdapter initialized with provider: {provider.name} ({getattr(provider,'model','-')})")

    @classmethod
    def auto(
        cls,
        prefer:      str = "ollama",          # "ollama" | "claude" | "rule-based"
        ollama_model: str = "llama3",
        claude_model: Optional[str] = None,
    ) -> "LLMAdapter":
        """
        Auto-detect and initialize the best available provider.

        Args:
            prefer:       Preferred provider. Falls back automatically if unavailable.
            ollama_model: Ollama model name.
            claude_model: Claude model string (defaults to haiku for cost).
        """
        candidates: list[LLMProvider] = []

        if prefer == "ollama":
            candidates = [
                OllamaProvider(model=ollama_model),
                ClaudeProvider(model=claude_model),
                RuleBasedProvider(),
            ]
        elif prefer == "claude":
            candidates = [
                ClaudeProvider(model=claude_model),
                OllamaProvider(model=ollama_model),
                RuleBasedProvider(),
            ]
        else:
            candidates = [RuleBasedProvider()]

        for p in candidates:
            try:
                if p.available():
                    log.info(f"Using LLM provider: {p.name}")
                    return cls(p)
            except Exception as e:
                log.debug(f"Provider {p.name} check failed: {e}")

        return cls(RuleBasedProvider())

    @classmethod
    def from_config(cls, config: dict) -> "LLMAdapter":
        """Initialize from ReconX config dict."""
        prefer = config.get("ai_provider", "ollama")
        return cls.auto(
            prefer=prefer,
            ollama_model=config.get("ollama_model", "llama3"),
            claude_model=config.get("claude_model", None),
        )

    # ── Delegate all calls to the active provider ────────────────────────────

    def ask(self, prompt: str, system: str = "", max_tokens: int = 1024) -> LLMResponse:
        return self._provider.ask(prompt, system=system, max_tokens=max_tokens)

    def analyze_findings(self, findings: list[dict], context: dict) -> LLMResponse:
        return self._provider.analyze_findings(findings, context)

    def generate_summary(self, report_data: dict) -> LLMResponse:
        return self._provider.generate_summary(report_data)

    def explain_cve(self, cve: str, service: str, target_context: str) -> LLMResponse:
        return self._provider.explain_cve(cve, service, target_context)

    def recommend_next_steps(self, context: dict) -> LLMResponse:
        return self._provider.recommend_next_steps(context)

    @property
    def provider_name(self) -> str:
        return self._provider.name

    @property
    def model_name(self) -> str:
        return getattr(self._provider, "model", "static")


# ── Prompt Templates ──────────────────────────────────────────────────────────

SECURITY_ANALYST_SYSTEM = """You are the ReconX AI Security Analyst — an embedded expert cybersecurity assistant.

Your role is to analyze reconnaissance findings, explain vulnerabilities in clear language,
correlate evidence into attack chains, and provide actionable defense recommendations.

Rules:
- Always distinguish between verified findings and inferred risks
- Structure responses clearly with sections and bullet points
- Prioritize by severity: CRITICAL > HIGH > MEDIUM > LOW
- Provide educational context — explain WHY something is a risk
- Give concrete remediation steps, not vague advice
- Never suggest illegal activity or harmful exploitation
- Be concise but complete — no unnecessary padding
"""


def _build_findings_prompt(findings: list[dict], context: dict) -> str:
    target   = context.get("target", "unknown")
    mode     = context.get("mode", "standard")
    services = context.get("services", [])

    findings_text = "\n".join(
        f"- [{f.get('severity','?')}] {f.get('title','?')} on {f.get('target','?')} "
        f"({f.get('service','?')}:{f.get('port','?')}) — CVE: {f.get('cve','none')}"
        for f in findings
    )

    services_text = ", ".join(
        f"{s.get('service','?')}:{s.get('port','?')}" for s in services[:15]
    )

    return f"""RECONX SECURITY ANALYSIS REQUEST
Target: {target}
Scan Mode: {mode}
Services Detected: {services_text}

FINDINGS ({len(findings)} total):
{findings_text}

ANALYSIS REQUIRED:
1. Executive Summary (2-3 sentences for non-technical stakeholders)
2. Critical Risks — what needs immediate attention and why
3. Attack Chains — which findings combine into multi-step exploits
4. Remediation Priority — ordered action list
5. Recommended Next Recon Steps — what to investigate further
"""


def _build_summary_prompt(report_data: dict) -> str:
    return f"""Generate an executive security report summary for:

Target: {report_data.get('target', 'unknown')}
Scan Date: {report_data.get('timestamp', 'unknown')}
Assets Discovered: {report_data.get('asset_count', 0)}
Open Ports: {report_data.get('open_ports', 0)}
Services: {report_data.get('service_count', 0)}
CVEs Matched: {len(report_data.get('cves', []))}
Critical Findings: {report_data.get('critical_count', 0)}
High Findings: {report_data.get('high_count', 0)}

Top Findings:
{chr(10).join(f"- {f}" for f in report_data.get('top_findings', [])[:5])}

Write a professional executive summary (3-4 paragraphs) suitable for a
security report. Include risk level assessment, key findings, business
impact, and recommended immediate actions.
"""


def _build_next_steps_prompt(context: dict) -> str:
    phase    = context.get("current_phase", "unknown")
    findings = context.get("findings_so_far", [])
    services = context.get("services", [])
    target   = context.get("target", "unknown")

    return f"""RECONX NEXT-STEP RECOMMENDATION

Target: {target}
Current Phase: {phase}
Services Found: {', '.join(str(s) for s in services[:10])}
Findings So Far: {len(findings)} ({context.get('critical_count', 0)} critical)

Based on this reconnaissance state, recommend the 3-5 most valuable next
investigation steps. For each step specify:
- What to do
- Which tool or technique
- Why it's valuable given the current findings
- Expected output

Prioritize steps that are most likely to reveal additional attack surface
or confirm critical risks.
"""
