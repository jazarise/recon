import ipaddress
import socket
from urllib.parse import urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from reconx.core.exceptions.errors import HttpError, DnsError

USER_AGENT = "ReconX/3.0.0"

def is_private_ip(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            return True
        # Explicit checks for fc00::/7 (Unique Local Addresses), wait ip.is_private covers it in Python 3.9+ for IPv6
        return False
    except ValueError:
        return False

def resolve_and_check_ssrf(url: str):
    """Resolves the hostname and checks against SSRF boundaries."""
    parsed = urlparse(url)
    hostname = parsed.hostname
    
    if not hostname:
        raise HttpError("Invalid URL: missing hostname")
        
    if hostname == "localhost":
        raise HttpError("SSRF attempt blocked: localhost")
        
    try:
        # Resolve all IPs
        addr_info = socket.getaddrinfo(hostname, None)
        ips = {info[4][0] for info in addr_info}
    except socket.gaierror as e:
        raise DnsError(f"DNS resolution failed for {hostname}: {e}")
        
    for ip in ips:
        if is_private_ip(ip):
            raise HttpError(f"SSRF attempt blocked: resolved to private IP {ip}")
            
    # For extra safety, you would ideally pin the request to the resolved IP, 
    # but strictly returning here enforces no internal domains if DNS doesn't trick us after.

class HttpClient:
    """Canonical Unified HTTP Client, preventing duplicate request wrappers."""
    
    _session = None

    @classmethod
    def get_session(cls) -> requests.Session:
        if cls._session is None:
            cls._session = requests.Session()
            cls._session.headers.update({"User-Agent": USER_AGENT})
            
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=frozenset(["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE", "TRACE"])
            )
            adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
            cls._session.mount("http://", adapter)
            cls._session.mount("https://", adapter)
            
        return cls._session

    @staticmethod
    def get(url: str, headers: dict = None, timeout: tuple = (5, 30)) -> dict:
        """Standard GET request wrapper returning clean status and body."""
        try:
            resolve_and_check_ssrf(url)
            session = HttpClient.get_session()
            resp = session.get(url, headers=headers, timeout=timeout)
            return {
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "body": resp.text,
                "error": None,
            }
        except Exception as e:
            return {
                "status_code": 0,
                "headers": {},
                "body": "",
                "error": str(e),
            }

    @staticmethod
    def post(url: str, json: dict = None, headers: dict = None, timeout: tuple = (5, 30)) -> dict:
        try:
            resolve_and_check_ssrf(url)
            session = HttpClient.get_session()
            resp = session.post(url, json=json, headers=headers, timeout=timeout)
            return {
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "body": resp.text,
                "error": None,
            }
        except Exception as e:
            return {
                "status_code": 0,
                "headers": {},
                "body": "",
                "error": str(e),
            }

    @staticmethod
    def request(method: str, url: str, headers: dict = None, timeout: tuple = (5, 30)) -> dict:
        try:
            resolve_and_check_ssrf(url)
            session = HttpClient.get_session()
            resp = session.request(method, url, headers=headers, timeout=timeout)
            return {
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "body": resp.text,
                "error": None,
            }
        except Exception as e:
            return {
                "status_code": 0,
                "headers": {},
                "body": "",
                "error": str(e),
            }
