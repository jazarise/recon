import socket
import subprocess
import platform
from core.models import Finding
from typing import List

class ActiveIpCollector:
    def __init__(self):
        self.ports = [80, 443, 22]

    def ping(self, ip: str) -> bool:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        cmd = ['ping', param, '1', '-w', '1000' if platform.system().lower() == 'windows' else '1', ip]
        try:
            res = subprocess.run(cmd, capture_output=True, timeout=2)
            return res.returncode == 0
        except Exception:
            return False

    def ptr_record(self, ip: str) -> str:
        try:
            name, _, _ = socket.gethostbyaddr(ip)
            return name
        except Exception:
            return ""

    def port_scan(self, ip: str) -> List[int]:
        open_ports = []
        for port in self.ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            try:
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
            except Exception:
                pass
            finally:
                sock.close()
        return open_ports

    def collect(self, target: str, **kwargs) -> list:
        try:
            ip = socket.gethostbyname(target)
        except socket.gaierror:
            return []

        findings = []
        
        if self.ping(ip):
            findings.append(Finding(
                category="active_ip_ping",
                source="active-ip",
                value=f"{ip} responded to ping",
                metadata={"ip": ip}
            ))
            
        ptr = self.ptr_record(ip)
        if ptr:
            findings.append(Finding(
                category="active_ip_ptr",
                source="active-ip",
                value=f"PTR record for {ip}: {ptr}",
                metadata={"ip": ip, "ptr": ptr}
            ))
            
        open_ports = self.port_scan(ip)
        if open_ports:
            findings.append(Finding(
                category="active_ip_ports",
                source="active-ip",
                value=f"Open ports on {ip}: {open_ports}",
                metadata={"ip": ip, "open_ports": open_ports}
            ))
            
        return findings
