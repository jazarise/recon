from core.plugin_manager.interface import ReconXPlugin
from core.schemas import IPAddress
import socket

class ActiveIPPlugin(ReconXPlugin):
    name = "active-ip"
    version = "1.0.0"
    description = "Resolve domains to active IPs"

    def run(self, target: str, **kwargs):
        try:
            ip = socket.gethostbyname(target)
            return {"ip": ip}
        except socket.gaierror:
            return {"ip": "127.0.0.1"} # Mock

    def normalize(self, results):
        if "ip" in results:
            return [IPAddress(value=results["ip"], source="active-ip")]
        return []
