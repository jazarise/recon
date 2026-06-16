class ScanSuppressor:
    def __init__(self):
        self.resolved_hosts = set()
    
    def check_and_add(self, host: str) -> bool:
        """Returns True if host is new, False if already scanned."""
        if host in self.resolved_hosts:
            return False
        self.resolved_hosts.add(host)
        return True
