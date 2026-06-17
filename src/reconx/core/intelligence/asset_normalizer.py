import re
from typing import Optional
from ipaddress import ip_address


class AssetNormalizer:
    @staticmethod
    def normalize_domain(domain: str) -> str:
        # Canonicalize to lowercase, strip trailing dots, strip whitespace
        return domain.strip().lower().rstrip(".")

    @staticmethod
    def normalize_url(url: str) -> str:
        # Strip trailing slashes, canonicalize scheme to lowercase
        url = url.strip()
        if not re.match(r"^https?://", url, re.IGNORECASE):
            url = f"http://{url}"

        # Lowercase scheme and host
        parsed = re.match(r"^(https?://)([^/:]+)(.*)$", url, re.IGNORECASE)
        if parsed:
            scheme, host, rest = parsed.groups()
            url = f"{scheme.lower()}{host.lower()}{rest}"

        return url.rstrip("/")

    @staticmethod
    def validate_ip(ip: str) -> Optional[str]:
        ip = ip.strip()
        try:
            return str(ip_address(ip))
        except ValueError:
            return None

    @staticmethod
    def is_safe_value(value: str) -> bool:
        # Reject malformed or dangerous inputs like ../../../etc/passwd or javascript:
        if ".." in value or "\x00" in value:
            return False
        if re.match(r"^(javascript|data):", value, re.IGNORECASE):
            return False
        return True
