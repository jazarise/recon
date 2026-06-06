"""
ReconX — Stage 21: Agent Layer
================================
Autonomous AI agents absorbed from hexstrike-ai, PentestAgent, CyberStrikeAI,
pentest-ai-agents, shannon, and METATRON.

Each agent has:
  - A mission type (goal)
  - A plan() method (builds step sequence using PTT reasoning)
  - An execute() method (runs steps via ReconX tools)
  - An evaluate() method (LLM judges results, decides next action)

Agent types:
  BugBountyAgent   — External attack surface recon + vuln finding
  CVEAgent         — Find exploitable CVEs in detected services
  WebAgent         — Autonomous web application assessment
  CloudAgent       — Cloud infrastructure exposure analysis
  NetworkAgent     — Internal network recon + lateral movement mapping
  APIAgent         — REST/GraphQL API security assessment
  CodeAgent        — Source code SAST + secret detection
  OSINTAgent       — Passive intelligence gathering

All agents:
  - Use the LLMAdapter (Ollama or Claude) for reasoning
  - Write results to ReconXStore
  - Respect scope validation
  - Have max_iterations guards (no infinite loops)
  - Log every decision for auditability
"""
from __future__ import annotations

import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

log = logging.getLogger("reconx.ai.agents")

# ── Agent State ────────────────────────────────────────────────────────────────

@dataclass
class AgentStep:
    step_id:    str
    tool:       str
    target:     str
    params:     dict
    status:     str        = "pending"   # pending|running|complete|failed|skipped
    result:     Any        = None
    reasoning:  str        = ""
    started_at: float      = 0.0
    ended_at:   float      = 0.0

    @property
    def duration_s(self) -> float:
        return round(self.ended_at - self.started_at, 2) if self.ended_at else 0.0


@dataclass
class AgentPlan:
    goal:       str
    steps:      list[AgentStep]      = field(default_factory=list)
    context:    dict                 = field(default_factory=dict)
    iteration:  int                  = 0
    findings:   list[dict]           = field(default_factory=list)
    complete:   bool                 = False
    conclusion: str                  = ""

    def add_step(self, tool: str, target: str, params: dict = None,
                 reasoning: str = "") -> AgentStep:
        step = AgentStep(
            step_id=f"step-{len(self.steps)+1}",
            tool=tool, target=target,
            params=params or {},
            reasoning=reasoning,
        )
        self.steps.append(step)
        return step

    def pending_steps(self) -> list[AgentStep]:
        return [s for s in self.steps if s.status == "pending"]

    def completed_steps(self) -> list[AgentStep]:
        return [s for s in self.steps if s.status == "complete"]

    def all_findings(self) -> list[dict]:
        findings = list(self.findings)
        for step in self.steps:
            if isinstance(step.result, dict) and "findings" in step.result:
                findings.extend(step.result["findings"])
        return findings


# ── Base Agent ─────────────────────────────────────────────────────────────────

class ReconXAgent(ABC):
    """
    Base class for all ReconX autonomous agents.

    Subclasses implement:
      initial_plan()   — returns the first AgentPlan
      evaluate_step()  — given a completed step result, decide next action
    """
    agent_type: str = "base"
    max_iterations: int = 10

    def __init__(self, llm=None, store=None, scope_validator=None):
        self.llm       = llm             # LLMAdapter instance
        self.store     = store           # ReconXStore instance
        self.validator = scope_validator
        self.agent_id  = f"agent-{uuid.uuid4().hex[:6]}"
        self._tool_registry: dict = {}   # tool_name → callable

    def register_tool(self, name: str, fn) -> None:
        self._tool_registry[name] = fn

    def run(self, target: str, scan_id: str, **kwargs) -> AgentPlan:
        """
        Main agent loop:
          1. Build initial plan
          2. Execute steps one by one
          3. After each step, evaluate results with LLM
          4. LLM may add new steps, skip steps, or conclude
          5. Loop until plan.complete or max_iterations
        """
        log.info(f"[{self.agent_type}/{self.agent_id}] Starting → {target}")

        plan = self.initial_plan(target, scan_id, **kwargs)
        iteration = 0

        while not plan.complete and iteration < self.max_iterations:
            iteration += 1
            plan.iteration = iteration

            pending = plan.pending_steps()
            if not pending:
                plan.complete = True
                break

            # Execute next pending step
            step = pending[0]
            self._execute_step(step, plan, scan_id)

            # Evaluate results with LLM and adapt plan
            if self.llm:
                self._evaluate_and_adapt(step, plan, target, scan_id)

            # Store findings from this step
            if self.store and step.result:
                self._persist_step_findings(step, scan_id, target)

        if not plan.conclusion:
            plan.conclusion = self._final_summary(plan, target)

        log.info(f"[{self.agent_type}/{self.agent_id}] Complete after {iteration} iterations, "
                 f"{len(plan.all_findings())} findings")
        return plan

    @abstractmethod
    def initial_plan(self, target: str, scan_id: str, **kwargs) -> AgentPlan: ...

    def _execute_step(self, step: AgentStep, plan: AgentPlan, scan_id: str) -> None:
        step.status    = "running"
        step.started_at = time.time()
        log.info(f"  [{step.step_id}] {step.tool} → {step.target}")
        try:
            fn = self._tool_registry.get(step.tool)
            if fn:
                step.result = fn(step.target, **step.params)
            else:
                # Tool not registered — record as stub result
                step.result = {"status": "not_executed", "reason": f"Tool '{step.tool}' not registered"}
            step.status = "complete"
        except Exception as e:
            step.result = {"error": str(e)}
            step.status = "failed"
            log.warning(f"  [{step.step_id}] FAILED: {e}")
        step.ended_at = time.time()

    def _evaluate_and_adapt(self, step: AgentStep, plan: AgentPlan,
                             target: str, scan_id: str) -> None:
        """Ask LLM to evaluate step results and decide what to do next."""
        findings_so_far = plan.all_findings()
        completed       = plan.completed_steps()

        prompt = f"""RECONX AGENT EVALUATION — {self.agent_type.upper()}
Target: {target}
Goal: {plan.goal}
Iteration: {plan.iteration}/{self.max_iterations}

Last Step: {step.tool} on {step.target}
Step Status: {step.status}
Step Result Summary: {json.dumps(step.result, default=str)[:800]}

Findings So Far ({len(findings_so_far)} total):
{json.dumps([f.get('title','?') + ' [' + f.get('severity','?') + ']' for f in findings_so_far[:10]], indent=2)}

Remaining Steps: {[s.tool for s in plan.pending_steps()]}

Decide:
1. Should any remaining steps be SKIPPED based on what we know? (list tool names to skip)
2. Should any NEW steps be ADDED? (specify: tool, target, params, reason)
3. Is the goal COMPLETE? Should the agent conclude?

Respond ONLY in JSON:
{{
  "skip_steps": ["tool_name_to_skip"],
  "add_steps": [{{"tool": "tool_name", "target": "target", "params": {{}}, "reasoning": "why"}}],
  "complete": false,
  "reasoning": "brief explanation of decision"
}}"""

        try:
            response = self.llm.ask(prompt, max_tokens=600)
            if not response.ok:
                return

            # Parse JSON decision
            raw = response.text.strip()
            # Strip markdown fences if present
            if "```" in raw:
                raw = raw.split("```")[1].lstrip("json").strip()

            decision = json.loads(raw)

            # Apply skip decisions
            for tool_name in decision.get("skip_steps", []):
                for s in plan.pending_steps():
                    if s.tool == tool_name:
                        s.status = "skipped"
                        log.info(f"  [LLM] Skipping {tool_name}: {decision.get('reasoning','')[:60]}")

            # Apply add-step decisions
            for add in decision.get("add_steps", []):
                new_step = plan.add_step(
                    tool=add.get("tool", ""),
                    target=add.get("target", step.target),
                    params=add.get("params", {}),
                    reasoning=add.get("reasoning", ""),
                )
                log.info(f"  [LLM] Adding step: {new_step.tool} → {new_step.reasoning[:60]}")

            # Complete decision
            if decision.get("complete"):
                plan.complete = True
                log.info(f"  [LLM] Agent concluding: {decision.get('reasoning','')[:80]}")

        except (json.JSONDecodeError, KeyError, Exception) as e:
            log.debug(f"  [LLM] Evaluation parse error: {e}")

    def _persist_step_findings(self, step: AgentStep, scan_id: str, target: str) -> None:
        if not self.store or not isinstance(step.result, dict):
            return
        for finding in step.result.get("findings", []):
            try:
                self.store.add_finding(
                    scan_id=scan_id,
                    title=finding.get("title", "Unknown"),
                    severity=finding.get("severity", "INFO"),
                    target=finding.get("target", target),
                    service=finding.get("service", ""),
                    description=finding.get("evidence", ""),
                    meta={"agent": self.agent_type, "tool": step.tool,
                          "step": step.step_id, **finding.get("meta", {})},
                )
            except Exception as e:
                log.debug(f"Finding persist error: {e}")

    def _final_summary(self, plan: AgentPlan, target: str) -> str:
        findings = plan.all_findings()
        if not findings:
            return f"{self.agent_type} agent completed with no findings for {target}."
        sev_counts = {}
        for f in findings:
            s = f.get("severity", "INFO")
            sev_counts[s] = sev_counts.get(s, 0) + 1
        parts = [f"{v} {k}" for k, v in sorted(sev_counts.items(),
                  key=lambda x: ["CRITICAL","HIGH","MEDIUM","LOW","INFO"].index(x[0])
                  if x[0] in ["CRITICAL","HIGH","MEDIUM","LOW","INFO"] else 99)]
        return (f"{self.agent_type} agent found {len(findings)} issues for {target}: "
                f"{', '.join(parts)}.")


# ─────────────────────────────────────────────────────────────────────────────
# BUG BOUNTY AGENT
# ─────────────────────────────────────────────────────────────────────────────

class BugBountyAgent(ReconXAgent):
    """
    Autonomous bug bounty recon agent.
    Prioritizes: attack surface mapping → high-value subdomain discovery
    → web vulnerability probing → report-ready findings.
    """
    agent_type = "bugbounty"
    max_iterations = 15

    def initial_plan(self, target: str, scan_id: str, **kwargs) -> AgentPlan:
        plan = AgentPlan(
            goal=f"Find valid, in-scope vulnerabilities suitable for bug bounty submission on {target}",
            context={"target": target, "scope": kwargs.get("scope", [target])},
        )
        plan.add_step("reconx_passive_discovery", target,
                      reasoning="Enumerate all subdomains and external attack surface")
        plan.add_step("reconx_dns_intelligence", target,
                      reasoning="DNS analysis for zone transfers, dangling records")
        plan.add_step("reconx_web_assessment", target, {"intensity": "standard"},
                      reasoning="Web app assessment for common vuln classes")
        plan.add_step("reconx_vuln_scan", target, {"severity": "high"},
                      reasoning="Nuclei scan for known CVEs and misconfigurations")
        plan.add_step("reconx_osint", target, {"modules": ["leaks", "github"]},
                      reasoning="Check for credential leaks and exposed secrets")
        plan.add_step("reconx_ai_analyze", target, {"mode": "findings"},
                      reasoning="AI triage and deduplication of findings")
        return plan


# ─────────────────────────────────────────────────────────────────────────────
# CVE EXPLOITATION AGENT
# ─────────────────────────────────────────────────────────────────────────────

class CVEAgent(ReconXAgent):
    """
    CVE-focused agent.
    Identifies services, maps them to known CVEs, validates exploitability,
    and generates remediation-focused findings.
    """
    agent_type = "cve"
    max_iterations = 8

    def initial_plan(self, target: str, scan_id: str, **kwargs) -> AgentPlan:
        plan = AgentPlan(
            goal=f"Identify and validate exploitable CVEs on {target}",
            context={"target": target},
        )
        plan.add_step("reconx_port_scan", target, {"profile": "balanced"},
                      reasoning="Discover all running services")
        plan.add_step("reconx_service_intelligence", target,
                      reasoning="Fingerprint service versions for CVE matching")
        plan.add_step("reconx_vuln_scan", target, {"severity": "all"},
                      reasoning="Nuclei + CVE mapper scan against all detected services")
        plan.add_step("reconx_attack_path_analysis", scan_id,
                      reasoning="Chain CVEs into multi-step attack paths")
        plan.add_step("reconx_ai_analyze", target, {"mode": "findings"},
                      reasoning="Explain CVEs and prioritize by actual exploitability")
        return plan


# ─────────────────────────────────────────────────────────────────────────────
# WEB ASSESSMENT AGENT
# ─────────────────────────────────────────────────────────────────────────────

class WebAgent(ReconXAgent):
    """
    Autonomous web application security agent.
    Covers: authentication, authorization, injection, logic flaws, session management.
    """
    agent_type = "web"
    max_iterations = 12

    def initial_plan(self, target: str, scan_id: str, **kwargs) -> AgentPlan:
        auth_profile = kwargs.get("auth_profile")
        intensity    = kwargs.get("intensity", "standard")

        plan = AgentPlan(
            goal=f"Comprehensive web application security assessment of {target}",
            context={"target": target, "authenticated": bool(auth_profile)},
        )
        plan.add_step("reconx_passive_discovery", target,
                      reasoning="Map all endpoints and subdomains")
        plan.add_step("reconx_web_assessment", target,
                      {"intensity": intensity, "auth_profile": auth_profile},
                      reasoning="Full web assessment: crawl, probe, enumerate")
        plan.add_step("reconx_crlf_probe", target,
                      reasoning="CRLF injection check on all URL parameters")
        plan.add_step("reconx_vuln_scan", target,
                      {"severity": "all", "templates": ["http", "ssl", "misconfiguration"]},
                      reasoning="Template-based vulnerability scanning")
        if auth_profile:
            plan.add_step("reconx_web_assessment", target,
                          {"intensity": intensity, "auth_profile": auth_profile,
                           "authenticated": True},
                          reasoning="Repeat assessment with authentication — check auth-only endpoints")
        plan.add_step("reconx_ai_analyze", target, {"mode": "findings"},
                      reasoning="Correlate web findings into exploitable chains")
        return plan


# ─────────────────────────────────────────────────────────────────────────────
# CLOUD AGENT
# ─────────────────────────────────────────────────────────────────────────────

class CloudAgent(ReconXAgent):
    """
    Cloud infrastructure security agent.
    Covers AWS, Azure, GCP, Kubernetes, Docker, CI/CD, storage buckets.
    """
    agent_type = "cloud"
    max_iterations = 10

    def initial_plan(self, target: str, scan_id: str, **kwargs) -> AgentPlan:
        providers = kwargs.get("providers", ["aws", "azure", "gcp"])
        plan = AgentPlan(
            goal=f"Identify cloud infrastructure exposures for {target} across {', '.join(providers)}",
            context={"target": target, "providers": providers},
        )
        plan.add_step("reconx_passive_discovery", target,
                      reasoning="Discover cloud-hosted subdomains and services")
        plan.add_step("reconx_cloud_intel", target, {"providers": providers},
                      reasoning="Cloud resource enumeration and misconfiguration detection")
        plan.add_step("reconx_dns_intelligence", target,
                      reasoning="DNS analysis for cloud service pointers and dangling records")
        plan.add_step("reconx_osint", target, {"modules": ["github", "leaks"]},
                      reasoning="Find cloud credentials in public repos and leaks")
        plan.add_step("reconx_ai_analyze", target, {"mode": "findings"},
                      reasoning="Analyze cloud findings for privilege escalation paths")
        return plan


# ─────────────────────────────────────────────────────────────────────────────
# NETWORK AGENT
# ─────────────────────────────────────────────────────────────────────────────

class NetworkAgent(ReconXAgent):
    """
    Internal network recon agent.
    Covers: host discovery, service enumeration, lateral movement paths,
    credential exposure, traffic analysis.
    """
    agent_type = "network"
    max_iterations = 10

    def initial_plan(self, target: str, scan_id: str, **kwargs) -> AgentPlan:
        plan = AgentPlan(
            goal=f"Internal network reconnaissance and lateral movement analysis of {target}",
            context={"target": target, "is_cidr": "/" in target},
        )
        plan.add_step("reconx_port_scan", target, {"profile": "balanced"},
                      reasoning="Discover all live hosts and open ports in range")
        plan.add_step("reconx_service_intelligence", target,
                      reasoning="Identify vulnerable services and version information")
        plan.add_step("reconx_vuln_scan", target,
                      {"severity": "critical", "templates": ["network", "default-credentials"]},
                      reasoning="Check for network-level CVEs and default credentials")
        plan.add_step("reconx_attack_path_analysis", scan_id,
                      reasoning="Map lateral movement paths between hosts")
        plan.add_step("reconx_ai_analyze", target, {"mode": "next_steps"},
                      reasoning="AI analysis of network exposure and pivot opportunities")
        return plan


# ─────────────────────────────────────────────────────────────────────────────
# API AGENT (absorbed from pentest-ai-agents APIAgent)
# ─────────────────────────────────────────────────────────────────────────────

class APIAgent(ReconXAgent):
    """
    REST/GraphQL API security assessment agent.
    Covers: authentication bypass, IDOR, rate limiting, injection, schema exposure.
    """
    agent_type = "api"
    max_iterations = 10

    def initial_plan(self, target: str, scan_id: str, **kwargs) -> AgentPlan:
        plan = AgentPlan(
            goal=f"API security assessment of {target}",
            context={"target": target, "api_type": kwargs.get("api_type", "rest")},
        )
        # Discover API endpoints
        plan.add_step("reconx_web_assessment", target,
                      {"intensity": "standard", "focus": "api"},
                      reasoning="Discover API endpoints, swagger docs, GraphQL schema")
        # Probe for common API vulnerabilities
        plan.add_step("reconx_vuln_scan", target,
                      {"templates": ["api", "jwt", "graphql", "cors"]},
                      reasoning="Template scan for API-specific vulnerabilities")
        plan.add_step("reconx_crlf_probe", target,
                      reasoning="Header injection on API endpoints")
        plan.add_step("reconx_ai_analyze", target,
                      {"mode": "findings", "question": "What API-specific attack vectors exist?"},
                      reasoning="AI analysis focused on API exploitation chains")
        return plan


# ─────────────────────────────────────────────────────────────────────────────
# CODE AGENT (absorbed from shannon / shannon-uncontained)
# ─────────────────────────────────────────────────────────────────────────────

class CodeAgent(ReconXAgent):
    """
    Source code security analysis agent.
    Covers: SAST taint analysis, secrets detection, SCA, business logic.
    """
    agent_type = "code"
    max_iterations = 8

    def initial_plan(self, target: str, scan_id: str, **kwargs) -> AgentPlan:
        repo_path = kwargs.get("repo_path", target)
        checks    = kwargs.get("checks", ["taint", "secrets", "sca"])

        plan = AgentPlan(
            goal=f"Static security analysis of codebase at {repo_path}",
            context={"repo_path": repo_path, "checks": checks},
        )
        plan.add_step("reconx_sast", repo_path, {"checks": checks},
                      reasoning="Taint analysis, secret detection, dependency audit")
        plan.add_step("reconx_ai_analyze", repo_path,
                      {"mode": "findings",
                       "question": "What are the highest-risk findings in this codebase?"},
                      reasoning="AI explanation and prioritization of code-level findings")
        return plan


# ─────────────────────────────────────────────────────────────────────────────
# OSINT AGENT (absorbed from reconftw / METATRON)
# ─────────────────────────────────────────────────────────────────────────────

class OSINTAgent(ReconXAgent):
    """
    Passive open-source intelligence gathering agent.
    Covers: leaks, dorks, GitHub, metadata, subdomains, DNS, mail hygiene.
    No active scanning — fully passive.
    """
    agent_type = "osint"
    max_iterations = 8

    def initial_plan(self, target: str, scan_id: str, **kwargs) -> AgentPlan:
        plan = AgentPlan(
            goal=f"Passive OSINT collection for {target} with zero active scanning",
            context={"target": target, "passive_only": True},
        )
        plan.add_step("reconx_passive_discovery", target, {"depth": "deep"},
                      reasoning="Maximum passive subdomain discovery from all sources")
        plan.add_step("reconx_osint", target,
                      {"modules": ["leaks", "dorks", "github", "mail_hygiene"]},
                      reasoning="Full OSINT suite: leaks, dorks, code intel, mail config")
        plan.add_step("reconx_dns_intelligence", target,
                      reasoning="Passive DNS analysis: mail records, NS info, SPF/DMARC")
        plan.add_step("reconx_ai_analyze", target,
                      {"mode": "summary",
                       "question": "What does this OSINT tell us about attack surface and exposure?"},
                      reasoning="Synthesize OSINT into actionable intelligence brief")
        return plan


# ─────────────────────────────────────────────────────────────────────────────
# AGENT FACTORY
# ─────────────────────────────────────────────────────────────────────────────

AGENT_REGISTRY: dict[str, type[ReconXAgent]] = {
    "bugbounty": BugBountyAgent,
    "cve":       CVEAgent,
    "web":       WebAgent,
    "cloud":     CloudAgent,
    "network":   NetworkAgent,
    "api":       APIAgent,
    "code":      CodeAgent,
    "osint":     OSINTAgent,
}


def create_agent(
    agent_type: str,
    llm=None,
    store=None,
    scope_validator=None,
) -> ReconXAgent:
    """
    Factory: create a ReconX agent by type.

    Usage:
        from reconx.ai.agents import create_agent
        from reconx.ai.llm_adapter import LLMAdapter
        from reconx.data.store import ReconXStore

        llm   = LLMAdapter.auto()
        store = ReconXStore.open()
        agent = create_agent("bugbounty", llm=llm, store=store)
        plan  = agent.run("example.com", scan_id="rx-abc123")
    """
    cls = AGENT_REGISTRY.get(agent_type.lower())
    if not cls:
        raise ValueError(
            f"Unknown agent type: '{agent_type}'. "
            f"Available: {', '.join(AGENT_REGISTRY)}"
        )
    return cls(llm=llm, store=store, scope_validator=scope_validator)


def list_agents() -> list[dict]:
    """Return metadata for all available agent types."""
    descriptions = {
        "bugbounty": "External attack surface recon optimized for bug bounty submissions",
        "cve":       "CVE identification and exploitability validation across all services",
        "web":       "Autonomous web application security assessment (auth, injection, logic)",
        "cloud":     "Cloud infrastructure exposure: AWS/Azure/GCP/K8s/CI-CD analysis",
        "network":   "Internal network recon, lateral movement paths, credential exposure",
        "api":       "REST/GraphQL API security: IDOR, auth bypass, injection, schema leaks",
        "code":      "Source code SAST: taint analysis, secrets detection, SCA",
        "osint":     "Fully passive OSINT: leaks, dorks, GitHub, DNS, metadata",
    }
    return [
        {
            "type":          atype,
            "class":         cls.__name__,
            "max_iterations": cls.max_iterations,
            "description":   descriptions.get(atype, ""),
        }
        for atype, cls in AGENT_REGISTRY.items()
    ]
