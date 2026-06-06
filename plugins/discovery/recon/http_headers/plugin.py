from core.http.client import HttpClient
import aiohttp


class Plugin:
    name = 'http_headers'
    category = 'recon'
    async def run(target: str, context: dict) -> dict -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}
        
        if not target.startswith("http"):
            target = "https://" + target

        try:
            async with HttpClient() as session:
                async with session.get(target, timeout=10, allow_redirects=True) as resp:
                    headers = dict(resp.headers)
                    assets = []
                    findings = []
                    
                    if "Server" in headers:
                        assets.append({
                            "type": "technology",
                            "value": headers["Server"],
                            "tags": ["http_header", "server"]
                        })
                    
                    # Missing security headers
                    security_headers = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options"]
                    for sec in security_headers:
                        if sec not in headers:
                            findings.append({
                                "type": "missing_header",
                                "severity": "low",
                                "title": f"Missing {sec}",
                                "description": f"The target is missing the {sec} header."
                            })

                    return {
                        "assets": assets,
                        "findings": findings,
                        "metadata": {"raw_headers": headers}
                    }
        except Exception as e:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "HTTP Header Error", "description": str(e)}], "metadata": {}}
