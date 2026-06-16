import re
from urllib.parse import urlparse, urlunparse

def normalize_url(url: str) -> str:
    """
    Normalize and validate a URL to prevent garbage data pollution in the database.
    Reject encoded newlines, control characters, invalid schemes, and quotes.
    Deduplicate slashes and remove trailing semicolons.
    """
    if not isinstance(url, str):
        return ""
        
    url = url.strip()
    
    # Reject strings containing obvious malicious/garbage bytes
    bad_chars = ["%0A", "%0D", "\n", "\r", "<", ">", '"', "'", "%0a", "%0d", "%22", "%27"]
    for bc in bad_chars:
        if bc in url:
            return ""
            
    # Reject lines that are probably command output (like [12:31:40])
    if re.search(r'^\[\d{2}:\d{2}:\d{2}\]', url):
        return ""
        
    # Strip trailing garbages commonly appended by bad parsers
    url = url.rstrip(';')
    
    try:
        parsed = urlparse(url)
    except ValueError:
        return ""
        
    # Must have a valid web scheme
    if parsed.scheme not in ["http", "https"]:
        return ""
        
    # Normalize path (remove duplicate slashes)
    path = parsed.path
    if path:
        path = re.sub(r'/{2,}', '/', path)
        
    # Reconstruct the sanitized URL
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    
    # Check for embedded URLs like http://scanme.org/http://blog.com
    # If the path part contains "http://" or "https://", it's usually a bad regex extraction from a tool
    if "http://" in normalized[8:] or "https://" in normalized[8:]:
        return ""
        
    return normalized
