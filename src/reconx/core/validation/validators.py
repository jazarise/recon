import re
import ipaddress
import unicodedata
from urllib.parse import urlparse
from reconx.core.exceptions.errors import ValidationError

MAX_DOMAIN_LENGTH = 253
MAX_URL_LENGTH = 2048
MAX_PATH_LENGTH = 4096

# Regex for a valid domain name
# It ensures labels are 1-63 chars long, alphanumeric or hyphen (not starting/ending with hyphen)
DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)

def normalize_input(value: str) -> str:
    """Normalize unicode input string to NFKC."""
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}")
    return unicodedata.normalize("NFKC", value.strip())

def validate_domain(domain: str) -> str:
    domain = normalize_input(domain)
    
    if len(domain) > MAX_DOMAIN_LENGTH:
        raise ValidationError(f"Domain exceeds maximum length of {MAX_DOMAIN_LENGTH}")
        
    if ".." in domain or "/" in domain or "@" in domain:
        raise ValidationError("Invalid characters in domain")
        
    # Strictly validate against domain regex
    if not DOMAIN_REGEX.match(domain):
        raise ValidationError("Invalid domain format")
        
    return domain

def validate_ipv4(ip: str) -> str:
    ip = normalize_input(ip)
    try:
        addr = ipaddress.IPv4Address(ip)
        return str(addr)
    except ipaddress.AddressValueError:
        raise ValidationError("Invalid IPv4 address")

def validate_ipv6(ip: str) -> str:
    ip = normalize_input(ip)
    try:
        addr = ipaddress.IPv6Address(ip)
        return str(addr)
    except ipaddress.AddressValueError:
        raise ValidationError("Invalid IPv6 address")

def validate_ip(ip: str) -> str:
    ip = normalize_input(ip)
    try:
        addr = ipaddress.ip_address(ip)
        return str(addr)
    except ValueError:
        raise ValidationError("Invalid IP address")

def validate_url(url: str) -> str:
    url = normalize_input(url)
    
    if len(url) > MAX_URL_LENGTH:
        raise ValidationError(f"URL exceeds maximum length of {MAX_URL_LENGTH}")
        
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValidationError(f"Invalid URL scheme: {parsed.scheme}. Only http/https are allowed.")
        
    if not parsed.netloc:
        raise ValidationError("URL must contain a network location (domain/IP)")
        
    return url

def validate_target(target: str) -> str:
    """Validates either a domain or an IP address."""
    target = normalize_input(target)
    
    try:
        return validate_ip(target)
    except ValidationError:
        pass
        
    try:
        return validate_domain(target)
    except ValidationError:
        raise ValidationError("Target must be a valid domain or IP address")

def validate_port(port: int) -> int:
    try:
        port_int = int(port)
    except (ValueError, TypeError):
        raise ValidationError("Port must be an integer")
        
    if not (1 <= port_int <= 65535):
        raise ValidationError("Port must be between 1 and 65535")
        
    return port_int

def validate_path(path: str) -> str:
    path = normalize_input(path)
    
    if len(path) > MAX_PATH_LENGTH:
        raise ValidationError(f"Path exceeds maximum length of {MAX_PATH_LENGTH}")
        
    if "../" in path or "..\\" in path:
        raise ValidationError("Path traversal (../) is not allowed")
        
    return path
