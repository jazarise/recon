import socket

class DnsClient:
    """Canonical Unified DNS Resolver, replacing repetitive custom scripts."""
    
    @staticmethod
    def resolve_a(domain: str) -> list:
        """Resolves A records natively."""
        try:
            _, _, ipaddrlist = socket.gethostbyname_ex(domain)
            return ipaddrlist
        except Exception:
            return []
