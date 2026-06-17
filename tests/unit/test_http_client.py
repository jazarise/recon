import pytest
from unittest.mock import patch, MagicMock
from reconx.core.utils.http_client import HttpClient, is_private_ip, resolve_and_check_ssrf
from reconx.core.exceptions.errors import HttpError, DnsError
import requests

def test_is_private_ip():
    assert is_private_ip("127.0.0.1") is True
    assert is_private_ip("10.0.0.5") is True
    assert is_private_ip("192.168.1.1") is True
    assert is_private_ip("172.16.0.1") is True
    assert is_private_ip("169.254.169.254") is True
    assert is_private_ip("8.8.8.8") is False
    assert is_private_ip("fc00::1") is True
    assert is_private_ip("::1") is True

@patch("reconx.core.utils.http_client.socket.getaddrinfo")
def test_resolve_and_check_ssrf_safe(mock_getaddrinfo):
    # Mocking socket resolution for a safe IP
    mock_getaddrinfo.return_value = [(2, 1, 6, '', ('8.8.8.8', 80))]
    resolve_and_check_ssrf("http://example.com")
    mock_getaddrinfo.assert_called_with("example.com", None)

@patch("reconx.core.utils.http_client.socket.getaddrinfo")
def test_resolve_and_check_ssrf_unsafe(mock_getaddrinfo):
    mock_getaddrinfo.return_value = [(2, 1, 6, '', ('127.0.0.1', 80))]
    with pytest.raises(HttpError) as exc:
        resolve_and_check_ssrf("http://localhost.mali_domain.com")
    assert "private IP" in str(exc.value)

def test_resolve_and_check_ssrf_localhost():
    with pytest.raises(HttpError):
        resolve_and_check_ssrf("http://localhost:8080")

@patch("reconx.core.utils.http_client.requests.Session")
def test_http_client_get(mock_session_cls):
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.text = "Success"
    mock_session.get.return_value = mock_response
    mock_session_cls.return_value = mock_session
    
    # We must patch SSRF check to avoid actual DNS lookups in tests
    with patch("reconx.core.utils.http_client.resolve_and_check_ssrf"):
        res = HttpClient.get("http://example.com")
        
    assert res["status_code"] == 200
    assert res["body"] == "Success"
    assert res["error"] is None
