def enrich_ip_geo(ip: str) -> dict:
    """Simulates IP-API unauthenticated GeoLocation extraction."""
    # Mock return for Stage 11
    return {
        "ip": ip,
        "country": "US",
        "asn": "AS15169 Google LLC"
    }

def analyze_security_headers(headers: dict) -> list:
    """Detects missing security headers from raw responses."""
    missing = []
    if "Strict-Transport-Security" not in headers:
        missing.append("Missing HSTS")
    if "X-Frame-Options" not in headers:
        missing.append("Missing X-Frame-Options")
    return missing
