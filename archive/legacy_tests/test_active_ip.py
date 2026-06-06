import pytest
from unittest.mock import patch, MagicMock
from modules.recon.active_ip.plugin import Plugin
from core.models import Finding

@patch('modules.recon.active_ip.collector.socket.gethostbyaddr')
@patch('modules.recon.active_ip.collector.socket.gethostbyname')
@patch('modules.recon.active_ip.collector.socket.socket')
@patch('modules.recon.active_ip.collector.subprocess.run')
def test_active_ip_execution(mock_run, mock_socket, mock_gethostbyname, mock_gethostbyaddr):
    mock_run.return_value = MagicMock(returncode=0) # ping success
    mock_gethostbyname.return_value = "8.8.8.8"
    mock_gethostbyaddr.return_value = ("dns.google", [], ["8.8.8.8"])
    
    mock_sock_instance = MagicMock()
    mock_sock_instance.connect_ex.return_value = 0 # port open
    mock_socket.return_value = mock_sock_instance
    
    plugin = Plugin()
    findings = plugin.run("8.8.8.8")
    
    assert len(findings) == 3
    assert all(isinstance(f, Finding) for f in findings)
    
    types = [f.category for f in findings]
    assert "active_ip_ping" in types
    assert "active_ip_ptr" in types
    assert "active_ip_ports" in types
