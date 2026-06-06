"""
ReconX — Engagement Engine
============================
Absorbed from pentest-ai engine/core.py, engine/auth.py, engine/rate_limit.py.

Components:
  Engagement          — scan session lifecycle (start/status/stop/resume)
  RateLimitGovernor   — HTTP 429 exponential backoff + per-host throttle
  AuthResolver        — JWT login, cookie capture, Basic auth injection
  WordlistLocator     — SecLists/kali/custom wordlist auto-detection chain
  EngagementManager   — top-level coordinator managing multiple engagements

Usage:
    eng = EngagementManager.start("example.com", mode="balanced")
    eng.configure_auth("admin", "password", login_url="https://example.com/login")
    results = eng.run_tool("ffuf", extra_args=["-w", eng.wordlist("directories")])
    eng.stop()
"""
from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import re
import shutil
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Optional

log = logging.getLogger("reconx.engine.engagement")

# ── Rate limit defaults ───────────────────────────────────────────────────────

_DEFAULT_DELAY    = 0.25   # seconds between requests to same host
_MAX_RETRIES      = 5
_BACKOFF_BASE     = 2.0    # exponential backoff multiplier
_MAX_BACKOFF      = 60.0   # cap backoff at 60s

# ── Wordlist search paths ─────────────────────────────────────────────────────

_WORDLIST_CANDIDATES = {
    "directories": [
        "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt",
        "/usr/share/seclists/Discovery/Web-Content/common.txt",
        "/usr/share/wordlists/dirb/common.txt",
        "/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt",
        "wordlists/directories.txt",
    ],
    "subdomains": [
        "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
        "/usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt",
        "/usr/share/wordlists/subdomains.txt",
        "wordlists/subdomains.txt",
    ],
    "passwords": [
        "/usr/share/seclists/Passwords/darkweb2017-top100.txt",
        "/usr/share/wordlists/rockyou.txt",
        "/usr/share/wordlists/fasttrack.txt",
        "wordlists/passwords.txt",
    ],
    "usernames": [
        "/usr/share/seclists/Usernames/top-usernames-shortlist.txt",
        "/usr/share/seclists/Usernames/Names/names.txt",
        "/usr/share/wordlists/metasploit/unix_users.txt",
        "wordlists/usernames.txt",
    ],
    "api_paths": [
        "/usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt",
        "/usr/share/seclists/Discovery/Web-Content/swagger.txt",
        "wordlists/api_paths.txt",
    ],
    "virtual_hosts": [
        "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
        "wordlists/vhosts.txt",
    ],
}


# ── Rate Limit Governor ───────────────────────────────────────────────────────

class RateLimitGovernor:
    """
    Per-host request throttling with HTTP 429 exponential backoff.
    Absorbed from pentest-ai engine/rate_limit.py.

    Thread-safe — shared across concurrent tool executions.
    """

    def __init__(self, delay: float = _DEFAULT_DELAY):
        self._delay        = delay
        self._last_req:    dict[str, float] = {}   # host → timestamp
        self._retry_after: dict[str, float] = {}   # host → backoff until
        self._lock         = Lock()

    def wait(self, host: str) -> None:
        """Block until it's safe to send another request to this host."""
        with self._lock:
            now = time.time()

            # Check if we're in a retry-after window
            until = self._retry_after.get(host, 0)
            if now < until:
                wait_s = until - now
                log.debug("RateLimit backoff: %s — sleeping %.1fs", host, wait_s)

            last = self._last_req.get(host, 0)
            gap  = now - last
            if gap < self._delay:
                time.sleep(self._delay - gap)

            self._last_req[host] = time.time()

    def on_429(self, host: str, retry_after_header: Optional[str] = None,
               attempt: int = 1) -> float:
        """
        Called when a 429 is received. Computes and stores backoff.
        Returns the number of seconds to wait.
        """
        with self._lock:
            if retry_after_header:
                try:
                    wait_s = float(retry_after_header)
                except ValueError:
                    wait_s = min(_BACKOFF_BASE ** attempt, _MAX_BACKOFF)
            else:
                wait_s = min(_BACKOFF_BASE ** attempt, _MAX_BACKOFF)

            self._retry_after[host] = time.time() + wait_s
            log.info("429 on %s — backing off %.1fs (attempt %d)", host, wait_s, attempt)
            return wait_s

    def request(self, url: str, method: str = "GET",
                data: Optional[bytes] = None,
                headers: Optional[dict] = None,
                timeout: int = 10) -> tuple[int, dict, str]:
        """
        Make a rate-limited HTTP request with automatic 429 retry.
        Returns (status, headers, body).
        """
        parsed = urllib.parse.urlparse(url)
        host   = parsed.netloc

        ua = {"User-Agent": "Mozilla/5.0 (ReconX; security-research)"}
        if headers:
            ua.update(headers)

        for attempt in range(1, _MAX_RETRIES + 1):
            self.wait(host)
            try:
                req = urllib.request.Request(url, data=data, headers=ua, method=method)
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    body = resp.read(131072).decode("utf-8", errors="ignore")
                    return resp.status, dict(resp.headers), body
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    ra = e.headers.get("Retry-After")
                    wait_s = self.on_429(host, ra, attempt)
                    time.sleep(wait_s)
                    continue
                body = e.read(32768).decode("utf-8", errors="ignore")
                return e.code, dict(e.headers), body
            except Exception as e:
                log.debug("Request error %s: %s", url, e)
                return 0, {}, ""

        return 429, {}, "[!] Max retries exceeded (repeated 429)"


# ── Auth Resolver ─────────────────────────────────────────────────────────────

@dataclass
class AuthProfile:
    name:       str
    auth_type:  str        # basic | bearer | jwt | cookie | apikey | none
    headers:    dict       = field(default_factory=dict)
    cookies:    dict       = field(default_factory=dict)
    token:      str        = ""
    acquired_at: float     = 0.0
    expires_in:  int       = 3600   # seconds


class AuthResolver:
    """
    Resolves authentication credentials and injects them into requests.
    Absorbed from pentest-ai engine/auth.py.

    Supports: Basic, Bearer token, JWT (auto-login), Cookie, API key.
    Profiles are named and reusable across tool executions.
    """

    def __init__(self, governor: Optional[RateLimitGovernor] = None):
        self._profiles: dict[str, AuthProfile] = {}
        self._active:   Optional[str] = None
        self._gov       = governor or RateLimitGovernor()

    def basic(self, name: str, username: str, password: str) -> AuthProfile:
        """Configure HTTP Basic authentication."""
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        p = AuthProfile(
            name=name, auth_type="basic",
            headers={"Authorization": f"Basic {token}"},
        )
        self._profiles[name] = p
        return p

    def bearer(self, name: str, token: str) -> AuthProfile:
        """Configure Bearer token authentication."""
        p = AuthProfile(
            name=name, auth_type="bearer", token=token,
            headers={"Authorization": f"Bearer {token}"},
        )
        self._profiles[name] = p
        return p

    def apikey(self, name: str, key: str,
               header_name: str = "X-API-Key") -> AuthProfile:
        """Configure API key authentication."""
        p = AuthProfile(
            name=name, auth_type="apikey",
            headers={header_name: key},
        )
        self._profiles[name] = p
        return p

    def jwt_login(
        self, name: str,
        login_url: str,
        username: str, password: str,
        username_field: str = "email",
        password_field: str = "password",
        token_path: str = "token",           # dot-notation JSON path
        content_type: str = "application/json",
    ) -> AuthProfile:
        """
        Perform a login POST and extract JWT from JSON response.
        Stores the token for subsequent requests.
        """
        log.info("JWT login: %s as %s", login_url, username)

        if content_type == "application/json":
            payload = json.dumps({username_field: username, password_field: password}).encode()
        else:
            payload = urllib.parse.urlencode({username_field: username,
                                              password_field: password}).encode()

        status, headers, body = self._gov.request(
            login_url, method="POST", data=payload,
            headers={"Content-Type": content_type},
        )

        token = ""
        if status in (200, 201) and body:
            try:
                data  = json.loads(body)
                token = self._extract_json_path(data, token_path) or ""
            except Exception:
                # Try regex fallback for non-standard responses
                m = re.search(r'"(?:token|access_token|jwt)"\s*:\s*"([^"]{20,})"', body)
                if m:
                    token = m.group(1)

        if not token:
            log.warning("JWT login failed (status=%d): could not extract token via path=%s",
                        status, token_path)

        p = AuthProfile(
            name=name, auth_type="jwt", token=token,
            headers={"Authorization": f"Bearer {token}"} if token else {},
            acquired_at=time.time(),
        )
        self._profiles[name] = p
        return p

    def cookie_capture(self, name: str, login_url: str,
                       username: str, password: str,
                       username_field: str = "username",
                       password_field: str = "password") -> AuthProfile:
        """
        Perform login and capture Set-Cookie headers for session authentication.
        """
        payload = urllib.parse.urlencode({
            username_field: username, password_field: password
        }).encode()

        _, resp_headers, _ = self._gov.request(
            login_url, method="POST", data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        cookies: dict[str, str] = {}
        for key, val in resp_headers.items():
            if key.lower() == "set-cookie":
                m = re.match(r"([^=]+)=([^;]+)", val)
                if m:
                    cookies[m.group(1).strip()] = m.group(2).strip()

        cookie_header = "; ".join(f"{k}={v}" for k, v in cookies.items())
        p = AuthProfile(
            name=name, auth_type="cookie",
            cookies=cookies,
            headers={"Cookie": cookie_header} if cookie_header else {},
        )
        self._profiles[name] = p
        return p

    def get_headers(self, profile_name: Optional[str] = None) -> dict:
        """Return auth headers for the named (or active) profile."""
        name = profile_name or self._active
        if not name:
            return {}
        p = self._profiles.get(name)
        return dict(p.headers) if p else {}

    def set_active(self, name: str) -> None:
        self._active = name

    def list_profiles(self) -> list[str]:
        return list(self._profiles.keys())

    @staticmethod
    def _extract_json_path(data: dict, path: str) -> Optional[str]:
        """Extract value from nested dict using dot-notation path."""
        current = data
        for key in path.split("."):
            if isinstance(current, dict):
                current = current.get(key)
            else:
                return None
        return str(current) if current is not None else None


# ── Wordlist Locator ──────────────────────────────────────────────────────────

class WordlistLocator:
    """
    Auto-detect wordlists from SecLists, Kali, Parrot, or custom locations.
    Absorbed from pentest-ai tools/plugin_loader.py wordlist resolution.
    """

    def find(self, category: str, fallback_generate: bool = True) -> Optional[str]:
        """
        Return path to a usable wordlist for the given category.

        Args:
            category:          One of: directories, subdomains, passwords,
                               usernames, api_paths, virtual_hosts
            fallback_generate: If True, generate a minimal built-in list
                               when nothing is found on disk.

        Returns:
            Absolute path string, or None if unavailable and no fallback.
        """
        candidates = _WORDLIST_CANDIDATES.get(category, [])
        for path in candidates:
            if os.path.exists(path) and os.path.getsize(path) > 0:
                log.debug("Wordlist found: %s → %s", category, path)
                return path

        if fallback_generate:
            return self._generate_builtin(category)

        log.warning("No wordlist found for category '%s'", category)
        return None

    def _generate_builtin(self, category: str) -> str:
        """Write a minimal built-in wordlist to ~/.reconx/wordlists/."""
        builtin: dict[str, list[str]] = {
            "directories": [
                "admin", "api", "backup", "config", "dashboard", "data",
                "debug", "dev", "files", "images", "includes", "install",
                "js", "login", "manage", "old", "phpinfo", "robots.txt",
                "server-status", "setup", "static", "test", "upload",
                "v1", "v2", "vendor", "wp-admin", "wp-login.php",
            ],
            "subdomains": [
                "www", "mail", "ftp", "smtp", "pop", "imap", "webmail",
                "api", "dev", "staging", "test", "uat", "admin", "portal",
                "cdn", "static", "assets", "img", "blog", "shop", "store",
                "app", "mobile", "gateway", "vpn", "remote", "secure",
            ],
            "passwords": [
                "admin", "password", "123456", "password123", "admin123",
                "letmein", "qwerty", "welcome", "root", "toor", "pass",
                "test", "1234", "12345678", "default", "changeme",
            ],
            "usernames": [
                "admin", "administrator", "root", "user", "test", "guest",
                "info", "support", "mail", "contact", "webmaster", "service",
            ],
            "api_paths": [
                "/api", "/api/v1", "/api/v2", "/api/v3",
                "/swagger.json", "/openapi.json", "/api-docs",
                "/graphql", "/graphiql", "/.well-known/openapi.yaml",
                "/api/health", "/api/status", "/api/version",
            ],
        }

        wl_dir = Path.home() / ".reconx" / "wordlists"
        wl_dir.mkdir(parents=True, exist_ok=True)
        wl_path = wl_dir / f"{category}_builtin.txt"

        entries = builtin.get(category, ["test"])
        if not wl_path.exists() or wl_path.stat().st_size == 0:
            wl_path.write_text("\n".join(entries), encoding="utf-8")
            log.info("Generated built-in wordlist: %s (%d entries)", wl_path, len(entries))

        return str(wl_path)


# ── Engagement ────────────────────────────────────────────────────────────────

@dataclass
class EngagementStatus:
    id:          str
    target:      str
    mode:        str
    status:      str        # created|running|paused|complete|failed
    started_at:  float
    stopped_at:  float      = 0.0
    tool_count:  int        = 0
    finding_count: int      = 0
    session_id:  Optional[int] = None


class Engagement:
    """
    Single scan engagement — lifecycle manager.
    Absorbed from pentest-ai EngagementSession.

    Manages:
      - Scan state (start/pause/stop/resume)
      - Auth profiles for this engagement
      - Rate limiting per target host
      - Wordlist resolution
      - Tool execution context
    """

    def __init__(
        self, target: str, mode: str = "balanced",
        session_id: Optional[int] = None,
    ):
        import uuid
        self.id         = f"rx-{uuid.uuid4().hex[:8]}"
        self.target     = target
        self.mode       = mode
        self.session_id = session_id
        self.status     = "created"
        self.started_at = time.time()

        self._governor  = RateLimitGovernor()
        self._auth      = AuthResolver(governor=self._governor)
        self._wordlists = WordlistLocator()
        self._tool_log: list[dict] = []

        log.info("Engagement %s created: %s [%s]", self.id, target, mode)

    # ── Lifecycle ─────────────────────────────────────────────────────────

    def start(self) -> "Engagement":
        self.status     = "running"
        self.started_at = time.time()
        log.info("Engagement %s started", self.id)
        return self

    def pause(self) -> None:
        self.status = "paused"
        log.info("Engagement %s paused", self.id)

    def resume(self) -> None:
        self.status = "running"
        log.info("Engagement %s resumed", self.id)

    def stop(self) -> None:
        self.status     = "complete"
        self.stopped_at = time.time()
        log.info("Engagement %s stopped. Duration: %.1fs, Tools run: %d",
                 self.id, self.stopped_at - self.started_at, len(self._tool_log))

    def fail(self, reason: str = "") -> None:
        self.status = "failed"
        log.error("Engagement %s failed: %s", self.id, reason)

    # ── Auth delegation ───────────────────────────────────────────────────

    def configure_auth_basic(self, name: str, username: str, password: str) -> None:
        self._auth.basic(name, username, password)
        self._auth.set_active(name)

    def configure_auth_bearer(self, name: str, token: str) -> None:
        self._auth.bearer(name, token)
        self._auth.set_active(name)

    def configure_auth_jwt(self, name: str, login_url: str,
                            username: str, password: str,
                            **kwargs) -> bool:
        profile = self._auth.jwt_login(name, login_url, username, password, **kwargs)
        self._auth.set_active(name)
        return bool(profile.token)

    def configure_auth_cookie(self, name: str, login_url: str,
                               username: str, password: str) -> bool:
        profile = self._auth.cookie_capture(name, login_url, username, password)
        self._auth.set_active(name)
        return bool(profile.cookies)

    def auth_headers(self, profile: Optional[str] = None) -> dict:
        return self._auth.get_headers(profile)

    # ── Rate-limited request ──────────────────────────────────────────────

    def request(self, url: str, method: str = "GET",
                data: Optional[bytes] = None,
                extra_headers: Optional[dict] = None,
                timeout: int = 10) -> tuple[int, dict, str]:
        headers = self.auth_headers()
        if extra_headers:
            headers.update(extra_headers)
        return self._governor.request(url, method=method, data=data,
                                      headers=headers, timeout=timeout)

    # ── Wordlist access ───────────────────────────────────────────────────

    def wordlist(self, category: str) -> Optional[str]:
        return self._wordlists.find(category)

    # ── Tool logging ──────────────────────────────────────────────────────

    def log_tool(self, tool: str, target: str, duration_s: float,
                 finding_count: int = 0) -> None:
        self._tool_log.append({
            "tool": tool, "target": target,
            "duration_s": duration_s, "findings": finding_count,
            "ts": time.time(),
        })

    # ── Status snapshot ───────────────────────────────────────────────────

    def snapshot(self) -> EngagementStatus:
        return EngagementStatus(
            id=self.id, target=self.target, mode=self.mode,
            status=self.status, started_at=self.started_at,
            stopped_at=self.stopped_at,
            tool_count=len(self._tool_log),
            finding_count=sum(t["findings"] for t in self._tool_log),
            session_id=self.session_id,
        )


# ── Engagement Manager ────────────────────────────────────────────────────────

class EngagementManager:
    """
    Top-level coordinator for multiple concurrent engagements.
    Tracks active engagements and provides factory methods.
    """
    _active: dict[str, Engagement] = {}
    _lock   = Lock()

    @classmethod
    def start(cls, target: str, mode: str = "balanced",
              session_id: Optional[int] = None) -> Engagement:
        eng = Engagement(target, mode=mode, session_id=session_id)
        eng.start()
        with cls._lock:
            cls._active[eng.id] = eng
        return eng

    @classmethod
    def get(cls, engagement_id: str) -> Optional[Engagement]:
        return cls._active.get(engagement_id)

    @classmethod
    def list_all(cls) -> list[EngagementStatus]:
        with cls._lock:
            return [e.snapshot() for e in cls._active.values()]

    @classmethod
    def stop(cls, engagement_id: str) -> None:
        eng = cls._active.get(engagement_id)
        if eng:
            eng.stop()

    @classmethod
    def stop_all(cls) -> None:
        with cls._lock:
            for eng in cls._active.values():
                if eng.status == "running":
                    eng.stop()
