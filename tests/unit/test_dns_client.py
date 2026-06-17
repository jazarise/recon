import pytest
from unittest.mock import patch, MagicMock
from reconx.core.utils.dns_client import DnsClient
import dns.resolver

def test_dns_client_resolve_a_success():
    with patch("reconx.core.utils.dns_client.dns.resolver.Resolver.resolve") as mock_resolve:
        mock_ans = MagicMock()
        mock_ans.to_text.return_value = "1.2.3.4"
        mock_resolve.return_value = [mock_ans]
        
        client = DnsClient()
        res = client.resolve("example.com", "A")
        assert res["status"] == "NOERROR"
        assert res["records"] == ["1.2.3.4"]

def test_dns_client_nxdomain():
    with patch("reconx.core.utils.dns_client.dns.resolver.Resolver.resolve") as mock_resolve:
        mock_resolve.side_effect = dns.resolver.NXDOMAIN
        client = DnsClient()
        res = client.resolve("invalid.domain", "A")
        assert res["status"] == "NXDOMAIN"
        assert res["records"] == []

def test_dns_client_timeout():
    with patch("reconx.core.utils.dns_client.dns.resolver.Resolver.resolve") as mock_resolve:
        mock_resolve.side_effect = dns.resolver.Timeout
        client = DnsClient(retries=1)
        res = client.resolve("timeout.domain", "A")
        assert res["status"] == "TIMEOUT"
