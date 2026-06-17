import pytest
from reconx.core.validation.validators import (
    validate_domain,
    validate_ipv4,
    validate_ipv6,
    validate_ip,
    validate_url,
    validate_target,
    validate_port,
    validate_path,
)
from reconx.core.exceptions.errors import ValidationError

def test_validate_domain():
    assert validate_domain("google.com") == "google.com"
    assert validate_domain("sub.domain.com") == "sub.domain.com"
    assert validate_domain("example.co.uk") == "example.co.uk"
    
    with pytest.raises(ValidationError):
        validate_domain("...")
    with pytest.raises(ValidationError):
        validate_domain("..")
    with pytest.raises(ValidationError):
        validate_domain("@google.com")
    with pytest.raises(ValidationError):
        validate_domain("google.com/")
    with pytest.raises(ValidationError):
        validate_domain("../../../")

def test_validate_url():
    assert validate_url("http://example.com") == "http://example.com"
    assert validate_url("https://example.com/path") == "https://example.com/path"
    
    with pytest.raises(ValidationError):
        validate_url("file:///etc/passwd")
    with pytest.raises(ValidationError):
        validate_url("ftp://example.com")
    with pytest.raises(ValidationError):
        validate_url("gopher://example.com")
    with pytest.raises(ValidationError):
        validate_url("javascript:alert(1)")
    with pytest.raises(ValidationError):
        validate_url("data:text/html,<html>")

def test_validate_ip():
    assert validate_ipv4("192.168.1.1") == "192.168.1.1"
    with pytest.raises(ValidationError):
        validate_ipv4("256.256.256.256")
        
    assert validate_ipv6("::1") == "::1"
    with pytest.raises(ValidationError):
        validate_ipv6("192.168.1.1")
        
    assert validate_ip("10.0.0.1") == "10.0.0.1"
    assert validate_ip("fe80::1") == "fe80::1"

def test_validate_target():
    assert validate_target("google.com") == "google.com"
    assert validate_target("8.8.8.8") == "8.8.8.8"
    with pytest.raises(ValidationError):
        validate_target("http://google.com")

def test_validate_port():
    assert validate_port(80) == 80
    assert validate_port("443") == 443
    with pytest.raises(ValidationError):
        validate_port(0)
    with pytest.raises(ValidationError):
        validate_port(65536)
    with pytest.raises(ValidationError):
        validate_port("abc")

def test_validate_path():
    assert validate_path("/usr/local/bin") == "/usr/local/bin"
    with pytest.raises(ValidationError):
        validate_path("../../../etc/passwd")
    with pytest.raises(ValidationError):
        validate_path("..\\..\\windows\\system32")
