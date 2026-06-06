"""
ReconX — Service Enumeration Tools
=====================================
Absorbed from AutoRecon default-plugins — full working implementations.

Tools:
  DNSZoneTransfer    — dig AXFR zone transfer attempts
  DNSReverseLookup   — reverse PTR lookup on discovered IPs
  Enum4Linux         — Windows/Samba enumeration (enum4linux-ng preferred)
  SMBScanner         — nmap SMB scripts (nbstat, smb*, ssl*)
  LDAPEnumerator     — ldapsearch anonymous + auth enum
  KerberosEnumerator — nmap krb5-enum-users for AD recon
  MySQLScanner       — nmap mysql scripts
  MSSQLScanner       — nmap mssql scripts
  SecurityTxtFetcher — fetch .well-known/security.txt and robots.txt

All tools:
  - Return structured dict output compatible with ReconX findings schema
  - Handle tool-not-found gracefully
  - Respect timeouts
  - Sanitize all subprocess arguments
"""
from __future__ import annotations

import logging
import re
import shlex
import shutil
import socket
import subprocess
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

log = logging.getLogger("reconx.tools.service_enum")

_TIMEOUT_SHORT  = 30
_TIMEOUT_MEDIUM = 120
_TIMEOUT_LONG   = 300


def _run(cmd: list[str], timeout: int = _TIMEOUT_MEDIUM) -> tuple[str, str, int]:
    """Safe subprocess runner. Returns (stdout, stderr, returncode)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, errors="replace")
        return r.stdout, r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        return "", f"[!] Timed out after {timeout}s", -1
    except FileNotFoundError:
        return "", f"[!] Not found: {cmd[0]}", 127
    except Exception as e:
        return "", f"[!] Error: {e}", -1


def _tool_available(binary: str) -> bool:
    return shutil.which(binary) is not None


# ── DNS Zone Transfer ─────────────────────────────────────────────────────────

@dataclass
class ZoneTransferResult:
    target:    str
    nameserver: str
    domain:    str
    success:   bool
    records:   list[str] = field(default_factory=list)
    raw:       str = ""
    error:     str = ""


class DNSZoneTransfer:
    """
    Attempt AXFR zone transfer against discovered nameservers.
    Absorbed from AutoRecon/dns-zone-transfer.py.
    """

    def run(self, nameserver: str, domain: str) -> ZoneTransferResult:
        t0 = time.time()
        result = ZoneTransferResult(target=nameserver, nameserver=nameserver,
                                    domain=domain, success=False)

        if not _tool_available("dig"):
            result.error = "dig not found — install bind-utils"
            return result

        # Try AXFR against the nameserver for the domain
        cmd = ["dig", "AXFR", f"@{nameserver}", domain]
        log.info("Zone transfer: %s", " ".join(cmd))
        stdout, stderr, rc = _run(cmd, timeout=_TIMEOUT_SHORT)

        result.raw = stdout
        if "Transfer failed" in stdout or "REFUSED" in stdout or rc != 0:
            result.error = f"Zone transfer refused/failed (rc={rc})"
            if stderr:
                result.error += f": {stderr[:100]}"
            return result

        # Parse records from successful transfer
        records = []
        for line in stdout.splitlines():
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            # Valid DNS record lines: name ttl class type rdata
            parts = line.split()
            if len(parts) >= 4 and parts[2].upper() in ("IN", "ANY"):
                records.append(line)

        if records:
            result.success = True
            result.records = records
            log.info("Zone transfer SUCCESS: %d records from %s", len(records), nameserver)
        else:
            result.error = "Transfer completed but no records extracted"

        return result

    def run_all_ns(self, domain: str) -> list[ZoneTransferResult]:
        """Attempt zone transfer against all nameservers for a domain."""
        results = []

        # Get NS records first
        stdout, _, _ = _run(["dig", "+short", "NS", domain], timeout=_TIMEOUT_SHORT)
        nameservers = [ns.strip().rstrip(".") for ns in stdout.splitlines() if ns.strip()]

        if not nameservers:
            log.debug("No NS records found for %s", domain)
            return results

        for ns in nameservers:
            result = self.run(ns, domain)
            results.append(result)

        return results


# ── DNS Reverse Lookup ────────────────────────────────────────────────────────

class DNSReverseLookup:
    """Reverse PTR lookup for a list of IP addresses."""

    def lookup(self, ip: str) -> Optional[str]:
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except socket.herror:
            return None
        except Exception:
            return None

    def lookup_range(self, ips: list[str], threads: int = 20) -> dict[str, Optional[str]]:
        """Reverse lookup a list of IPs concurrently."""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        results: dict[str, Optional[str]] = {}
        with ThreadPoolExecutor(max_workers=threads) as pool:
            futures = {pool.submit(self.lookup, ip): ip for ip in ips}
            for fut in as_completed(futures):
                ip = futures[fut]
                results[ip] = fut.result()
        return results


# ── Enum4Linux ────────────────────────────────────────────────────────────────

@dataclass
class Enum4LinuxResult:
    target:    str
    tool_used: str
    success:   bool
    shares:    list[str] = field(default_factory=list)
    users:     list[str] = field(default_factory=list)
    groups:    list[str] = field(default_factory=list)
    domain:    str       = ""
    os_info:   str       = ""
    raw:       str       = ""
    error:     str       = ""


class Enum4Linux:
    """
    Windows/Samba enumeration using enum4linux or enum4linux-ng.
    Absorbed from AutoRecon/enum4linux.py.
    Prefers enum4linux-ng for better output structure.
    """

    def run(self, target: str) -> Enum4LinuxResult:
        result = Enum4LinuxResult(target=target, tool_used="", success=False)

        # Prefer enum4linux-ng
        if _tool_available("enum4linux-ng"):
            result.tool_used = "enum4linux-ng"
            cmd = ["enum4linux-ng", "-A", "-d", target]
        elif _tool_available("enum4linux"):
            result.tool_used = "enum4linux"
            cmd = ["enum4linux", "-a", "-M", "-l", "-d", target]
        else:
            result.error = "Neither enum4linux nor enum4linux-ng is installed"
            return result

        log.info("Enum4Linux: %s on %s", result.tool_used, target)
        stdout, stderr, rc = _run(cmd, timeout=_TIMEOUT_LONG)

        result.raw = stdout + ("\n[STDERR]\n" + stderr if stderr else "")

        if rc == 127:
            result.error = f"{result.tool_used} not found"
            return result

        # Parse shares
        result.shares = self._parse_shares(stdout)
        result.users  = self._parse_users(stdout)
        result.groups = self._parse_groups(stdout)
        result.domain = self._parse_domain(stdout)
        result.os_info= self._parse_os(stdout)
        result.success = bool(result.shares or result.users or result.domain)

        return result

    @staticmethod
    def _parse_shares(raw: str) -> list[str]:
        shares = []
        for line in raw.splitlines():
            m = re.search(r"Sharename\s+(.+)", line, re.IGNORECASE)
            if m:
                shares.append(m.group(1).strip())
            m2 = re.search(r"\s+(DISK|IPC|PRINT)\$?\s", line, re.IGNORECASE)
            if m2 and "|" in line:
                parts = line.split("|")
                if parts:
                    shares.append(parts[0].strip())
        return list(dict.fromkeys(shares))[:20]

    @staticmethod
    def _parse_users(raw: str) -> list[str]:
        users = []
        for line in raw.splitlines():
            m = re.search(r"user:\[([^\]]+)\]", line, re.IGNORECASE)
            if m:
                users.append(m.group(1).strip())
            m2 = re.search(r"^\s+(\w+)\s+\d+", line)
            if m2 and "user" in line.lower():
                users.append(m2.group(1))
        return list(dict.fromkeys(users))[:50]

    @staticmethod
    def _parse_groups(raw: str) -> list[str]:
        groups = []
        for line in raw.splitlines():
            m = re.search(r"group:\[([^\]]+)\]", line, re.IGNORECASE)
            if m:
                groups.append(m.group(1).strip())
        return list(dict.fromkeys(groups))[:20]

    @staticmethod
    def _parse_domain(raw: str) -> str:
        m = re.search(r"Domain Name:\s*(.+)", raw, re.IGNORECASE)
        return m.group(1).strip() if m else ""

    @staticmethod
    def _parse_os(raw: str) -> str:
        m = re.search(r"OS:\s*(.+)", raw, re.IGNORECASE)
        return m.group(1).strip() if m else ""


# ── SMB Scanner ───────────────────────────────────────────────────────────────

@dataclass
class SMBScanResult:
    target: str
    port:   int
    findings: list[dict] = field(default_factory=list)
    raw:    str = ""
    error:  str = ""


class SMBScanner:
    """
    Nmap SMB script scanning.
    Absorbed from AutoRecon/nmap-smb.py — runs nbstat, smb*, ssl* scripts.
    """

    def run(self, target: str, port: int = 445) -> SMBScanResult:
        result = SMBScanResult(target=target, port=port)

        if not _tool_available("nmap"):
            result.error = "nmap not found"
            return result

        cmd = [
            "nmap", "-sV", f"-p{port}",
            "--script=banner,(nbstat or smb* or ssl*) and not "
                           "(brute or broadcast or dos or external or fuzzer)",
            "-oN", "-",        # stdout
            "--open",
            target,
        ]
        log.info("SMB scan: nmap %s:%d", target, port)
        stdout, stderr, rc = _run(cmd, timeout=_TIMEOUT_MEDIUM)

        result.raw = stdout
        result.findings = self._parse_nmap_script_output(stdout)
        return result

    @staticmethod
    def _parse_nmap_script_output(raw: str) -> list[dict]:
        findings = []
        current_script = None
        for line in raw.splitlines():
            m = re.match(r"\|\s+(_[\w-]+):\s*(.*)", line)
            if m:
                current_script = m.group(1)
                val = m.group(2).strip()
                if val:
                    findings.append({"script": current_script, "output": val})
            elif current_script and line.startswith("|"):
                val = line.lstrip("| ").strip()
                if val and findings:
                    findings[-1]["output"] += " " + val
        return findings


# ── LDAP Enumerator ───────────────────────────────────────────────────────────

@dataclass
class LDAPResult:
    target:   str
    port:     int
    anon_ok:  bool = False
    base_dn:  str  = ""
    entries:  list[dict] = field(default_factory=list)
    raw:      str  = ""
    error:    str  = ""


class LDAPEnumerator:
    """
    LDAP anonymous enumeration using ldapsearch.
    Absorbed from AutoRecon/ldap-search.py.
    """

    def run(self, target: str, port: int = 389) -> LDAPResult:
        result = LDAPResult(target=target, port=port)

        if not _tool_available("ldapsearch"):
            result.error = "ldapsearch not found — install ldap-utils"
            return result

        # Step 1: Try anonymous bind to get rootDSE
        cmd = [
            "ldapsearch", "-x",
            "-H", f"ldap://{target}:{port}",
            "-s", "base",
            "-b", "",
            "(objectclass=*)",
            "namingContexts", "defaultNamingContext",
        ]
        log.info("LDAP rootDSE: %s:%d", target, port)
        stdout, stderr, rc = _run(cmd, timeout=_TIMEOUT_SHORT)

        result.raw = stdout
        if rc == 0 and "namingContexts" in stdout:
            result.anon_ok = True
            m = re.search(r"namingContexts:\s*(.+)", stdout, re.IGNORECASE)
            if m:
                result.base_dn = m.group(1).strip()

        # Step 2: If anonymous works, dump basic entries
        if result.anon_ok and result.base_dn:
            cmd2 = [
                "ldapsearch", "-x",
                "-H", f"ldap://{target}:{port}",
                "-b", result.base_dn,
                "-s", "sub",
                "(objectclass=*)",
                "cn", "sAMAccountName", "mail", "userPrincipalName",
            ]
            stdout2, _, _ = _run(cmd2, timeout=_TIMEOUT_MEDIUM)
            result.raw += "\n" + stdout2
            result.entries = self._parse_entries(stdout2)

        return result

    @staticmethod
    def _parse_entries(raw: str) -> list[dict]:
        entries: list[dict] = []
        current: dict = {}
        for line in raw.splitlines():
            if line.startswith("dn:"):
                if current:
                    entries.append(current)
                current = {"dn": line[3:].strip()}
            elif ":" in line and current:
                key, _, val = line.partition(":")
                current.setdefault(key.strip(), []).append(val.strip())
        if current:
            entries.append(current)
        return entries[:100]


# ── Kerberos Enumerator ───────────────────────────────────────────────────────

@dataclass
class KerberosResult:
    target:      str
    port:        int
    domain:      str
    valid_users: list[str] = field(default_factory=list)
    raw:         str = ""
    error:       str = ""


class KerberosEnumerator:
    """
    Kerberos user enumeration via nmap krb5-enum-users script.
    Absorbed from AutoRecon/nmap-kerberos.py.
    """

    def run(
        self, target: str, domain: str,
        username_wordlist: str = "/usr/share/seclists/Usernames/top-usernames-shortlist.txt",
        port: int = 88,
    ) -> KerberosResult:
        result = KerberosResult(target=target, port=port, domain=domain)

        if not _tool_available("nmap"):
            result.error = "nmap not found"
            return result

        import os
        if not os.path.exists(username_wordlist):
            # Fallback to minimal common username list
            result.error = f"Wordlist not found: {username_wordlist}"
            return result

        cmd = [
            "nmap", "-sV", f"-p{port}",
            "--script=banner,krb5-enum-users",
            f"--script-args=krb5-enum-users.realm={domain},userdb={username_wordlist}",
            "-oN", "-",
            target,
        ]
        log.info("Kerberos enum: %s domain=%s", target, domain)
        stdout, stderr, rc = _run(cmd, timeout=_TIMEOUT_LONG)
        result.raw = stdout

        # Parse valid usernames from nmap output
        for line in stdout.splitlines():
            m = re.search(r"Valid Username:\s*(.+)", line, re.IGNORECASE)
            if m:
                result.valid_users.append(m.group(1).strip())

        return result


# ── MySQL Scanner ─────────────────────────────────────────────────────────────

class MySQLScanner:
    """
    Nmap MySQL script scanning.
    Absorbed from AutoRecon/nmap-mysql.py.
    """

    def run(self, target: str, port: int = 3306) -> dict:
        if not _tool_available("nmap"):
            return {"error": "nmap not found", "target": target, "port": port}

        cmd = [
            "nmap", "-sV", f"-p{port}",
            "--script=banner,(mysql* or ssl*) and not "
                           "(brute or broadcast or dos or external or fuzzer)",
            "-oN", "-", target,
        ]
        stdout, stderr, rc = _run(cmd, timeout=_TIMEOUT_MEDIUM)
        version = ""
        m = re.search(r"mysql.*?(\d+\.\d+\.\d+)", stdout, re.IGNORECASE)
        if m:
            version = m.group(1)
        return {
            "target": target, "port": port,
            "version": version, "raw": stdout,
            "error": stderr if rc != 0 else "",
        }


# ── MSSQL Scanner ─────────────────────────────────────────────────────────────

class MSSQLScanner:
    """
    Nmap MSSQL script scanning.
    Absorbed from AutoRecon/nmap-mssql.py.
    """

    def run(self, target: str, port: int = 1433) -> dict:
        if not _tool_available("nmap"):
            return {"error": "nmap not found", "target": target, "port": port}

        cmd = [
            "nmap", "-sV", f"-p{port}",
            "--script=banner,(ms-sql* or ssl*) and not "
                           "(brute or broadcast or dos or external or fuzzer)",
            f"--script-args=mssql.instance-port={port},mssql.username=sa,mssql.password=sa",
            "-oN", "-", target,
        ]
        stdout, stderr, rc = _run(cmd, timeout=_TIMEOUT_MEDIUM)
        version = ""
        m = re.search(r"Microsoft SQL Server\s+(\d{4})", stdout, re.IGNORECASE)
        if m:
            version = m.group(1)
        return {
            "target": target, "port": port,
            "version": version, "raw": stdout,
            "error": stderr if rc != 0 else "",
        }


# ── Security.txt / Robots.txt Fetcher ─────────────────────────────────────────

@dataclass
class SecurityTxtResult:
    target:          str
    scheme:          str
    security_txt:    Optional[str]   = None
    robots_txt:      Optional[str]   = None
    disallowed:      list[str]       = field(default_factory=list)
    contacts:        list[str]       = field(default_factory=list)
    vulnerability_disclosure: str   = ""
    error:           str            = ""


class SecurityTxtFetcher:
    """
    Fetch and parse .well-known/security.txt and robots.txt.
    Absorbed from AutoRecon/curl-known-security.py and curl-robots.py.
    """
    _UA = "Mozilla/5.0 (ReconX Security Scanner; +https://reconx.io)"

    def run(self, target: str, port: int = 443) -> SecurityTxtResult:
        scheme = "https" if port in (443, 8443) else "http"
        base   = f"{scheme}://{target}:{port}" if port not in (80, 443) else f"{scheme}://{target}"
        result = SecurityTxtResult(target=target, scheme=scheme)

        result.security_txt = self._fetch(f"{base}/.well-known/security.txt")
        result.robots_txt   = self._fetch(f"{base}/robots.txt")

        if result.security_txt:
            result.contacts, result.vulnerability_disclosure = \
                self._parse_security_txt(result.security_txt)

        if result.robots_txt:
            result.disallowed = self._parse_robots(result.robots_txt)

        return result

    def _fetch(self, url: str) -> Optional[str]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": self._UA})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return resp.read(32768).decode("utf-8", errors="ignore")
        except Exception:
            pass
        return None

    @staticmethod
    def _parse_security_txt(content: str) -> tuple[list[str], str]:
        contacts: list[str] = []
        disclosure = ""
        for line in content.splitlines():
            line = line.strip()
            if line.lower().startswith("contact:"):
                contacts.append(line.split(":", 1)[1].strip())
            elif line.lower().startswith("policy:"):
                disclosure = line.split(":", 1)[1].strip()
        return contacts, disclosure

    @staticmethod
    def _parse_robots(content: str) -> list[str]:
        disallowed = []
        for line in content.splitlines():
            if line.strip().lower().startswith("disallow:"):
                path = line.split(":", 1)[1].strip()
                if path and path != "/":
                    disallowed.append(path)
        return disallowed[:50]


# ── Bruteforce Command Builder ────────────────────────────────────────────────

class BruteforceAdvisor:
    """
    Builds bruteforce command recommendations for manual execution.
    Absorbed from AutoRecon bruteforce plugins (SSH/FTP/SMB/RDP/HTTP).

    Does NOT automatically execute bruteforce — generates commands
    for operator review. This is by design for safety.
    """

    WORDLIST_USER = (
        "/usr/share/seclists/Usernames/top-usernames-shortlist.txt",
        "/usr/share/wordlists/metasploit/unix_users.txt",
        "usernames.txt",
    )
    WORDLIST_PASS = (
        "/usr/share/seclists/Passwords/darkweb2017-top100.txt",
        "/usr/share/wordlists/rockyou.txt",
        "passwords.txt",
    )

    def _find_list(self, candidates: tuple[str, ...]) -> str:
        import os
        for p in candidates:
            if os.path.exists(p):
                return p
        return candidates[-1]

    def commands_for_service(
        self, service: str, target: str, port: int
    ) -> list[str]:
        """
        Return a list of suggested bruteforce commands for a service.
        Operator must review and run these manually.
        """
        ul = self._find_list(self.WORDLIST_USER)
        pl = self._find_list(self.WORDLIST_PASS)
        cmds: list[str] = []

        svc = service.lower()

        if "ssh" in svc:
            cmds += [
                f'hydra -L "{ul}" -P "{pl}" -e nsr -s {port} -o ssh_hydra.txt ssh://{target}',
                f'medusa -U "{ul}" -P "{pl}" -e ns -n {port} -M ssh -h {target}',
            ]
        elif "ftp" in svc:
            cmds += [
                f'hydra -L "{ul}" -P "{pl}" -e nsr -s {port} -o ftp_hydra.txt ftp://{target}',
                f'medusa -U "{ul}" -P "{pl}" -e ns -n {port} -M ftp -h {target}',
            ]
        elif "smb" in svc or svc in ("microsoft-ds", "netbios"):
            cmds += [
                f'crackmapexec smb {target} --port={port} -u "{ul}" -p "{pl}"',
                f'hydra -L "{ul}" -P "{pl}" -s {port} -o smb_hydra.txt smb://{target}',
            ]
        elif "rdp" in svc or port == 3389:
            cmds += [
                f'hydra -L "{ul}" -P "{pl}" -s {port} -o rdp_hydra.txt rdp://{target}',
                f'ncrack -U "{ul}" -P "{pl}" --user administrator rdp://{target}:{port}',
            ]
        elif "http" in svc or svc == "www":
            cmds += [
                f'hydra -L "{ul}" -P "{pl}" -s {port} -f http-get://{target}',
            ]
        elif "ldap" in svc:
            cmds += [
                f'hydra -L "{ul}" -P "{pl}" -s {port} -o ldap_hydra.txt ldap://{target}',
            ]

        return cmds
