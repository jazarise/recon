from reconx.core.plugin_base import standardize_output
from reconx.core.http.client import HttpClient


class Plugin:
    name = 'surface_mapping'
    category = 'recon'
    async def analyze_headers(self, url: str) -> dict:
        # Ported functionality from WEBFANG surface mapping
        if not url.startswith("http"):
            url = "http://" + url
            
        try:
            async with HttpClient() as session:
                async with session.get(url, timeout=10, allow_redirects=True) as resp:
                    headers = resp.headers
                    status = resp.status
                    body = await resp.text()
                    return {"headers": dict(headers), "status": status, "body": body[:2000]}
        except Exception as e:
            return {"error": str(e)}

    def detect_technologies(self, headers: dict, body: str) -> list:
        techs = []
        server = headers.get("Server", "").lower()
        x_powered_by = headers.get("X-Powered-By", "").lower()
        
        # WEBFANG technology fingerprinting signatures
        if "nginx" in server: techs.append("Nginx")
        if "apache" in server: techs.append("Apache")
        if "cloudflare" in server: techs.append("Cloudflare")
        if "php" in x_powered_by or "php" in server: techs.append("PHP")
        if "express" in x_powered_by: techs.append("Express.js")
        if "asp.net" in x_powered_by: techs.append("ASP.NET")
        
        # Body signatures
        if "wp-content" in body: techs.append("WordPress")
        if "react" in body.lower() or "data-reactroot" in body: techs.append("React")
        if "vue" in body.lower(): techs.append("Vue.js")
        
        return list(set(techs))

    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}

        data = await self.analyze_headers(target)
        
        assets = []
        findings = []
        metadata = {}

        if "error" in data:
            findings.append({"type": "error", "severity": "info", "title": "Surface Mapping Error", "description": data["error"]})
        else:
            techs = self.detect_technologies(data.get("headers", {}), data.get("body", ""))
            
            for t in techs:
                assets.append({
                    "type": "technology",
                    "value": t,
                    "tags": ["webfang", "surface_mapping"]
                })
                
            metadata["headers"] = data.get("headers")
            metadata["status_code"] = data.get("status")

        return {
            "assets": assets,
            "findings": findings,
            "metadata": metadata
        }

# Auto-injected Metadata
PLUGIN_NAME = "surface_mapping"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for surface_mapping"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = ["aiohttp"]

PLUGIN_EXTERNAL_TOOLS = []
