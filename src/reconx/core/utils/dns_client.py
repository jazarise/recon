import dns.resolver
from dns.exception import DNSException
from reconx.core.exceptions.errors import DnsError

class DnsClient:
    """Canonical Unified DNS Resolver, replacing repetitive custom scripts."""
    
    def __init__(self, nameservers=None, timeout=2.0, lifetime=5.0, retries=3):
        self.resolver = dns.resolver.Resolver()
        if nameservers:
            self.resolver.nameservers = nameservers
        self.resolver.timeout = timeout
        self.resolver.lifetime = lifetime
        self.retries = retries

    def _execute_query(self, domain: str, rdtype: str) -> dict:
        for attempt in range(self.retries):
            try:
                answers = self.resolver.resolve(domain, rdtype)
                records = [rdata.to_text() for rdata in answers]
                return {
                    "records": records,
                    "status": "NOERROR",
                    "error": None
                }
            except dns.resolver.NXDOMAIN:
                return {"records": [], "status": "NXDOMAIN", "error": None}
            except dns.resolver.NoAnswer:
                return {"records": [], "status": "NOANSWER", "error": None}
            except dns.resolver.NoNameservers:
                return {"records": [], "status": "SERVFAIL", "error": "No nameservers answered"}
            except dns.resolver.Timeout:
                if attempt == self.retries - 1:
                    return {"records": [], "status": "TIMEOUT", "error": "Query timed out"}
                continue
            except Exception as e:
                return {"records": [], "status": "ERROR", "error": str(e)}
        
        return {"records": [], "status": "TIMEOUT", "error": "Max retries exceeded"}

    @staticmethod
    def resolve_a(domain: str) -> list:
        """Legacy compatibility method. Resolves A records natively."""
        client = DnsClient()
        res = client._execute_query(domain, "A")
        return res["records"]

    def resolve(self, domain: str, rdtype: str = "A") -> dict:
        return self._execute_query(domain, rdtype)
