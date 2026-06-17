from reconx.core.plugin_base import standardize_output
from reconx.core.http.client import HttpClient


class Plugin:
    name = 'tech_detection'
    category = 'recon'
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}
            
        if not target.startswith("http"):
            target = "https://" + target

        try:
            async with HttpClient() as session:
                async with session.get(target, timeout=10, allow_redirects=True) as resp:
                    headers = dict(resp.headers)
                    body = await resp.text()
                    
                    techs = set()
                    if "X-Powered-By" in headers:
                        techs.add(headers["X-Powered-By"])
                    if "Server" in headers:
                        techs.add(headers["Server"])
                    
                    if "wp-content" in body: techs.add("WordPress")
                    if "drupal" in body.lower(): techs.add("Drupal")
                    if "joomla" in body.lower(): techs.add("Joomla")
                    
                    assets = []
                    for t in techs:
                        assets.append({
                            "type": "technology",
                            "value": t,
                            "tags": ["tech_detection", "finalrecon"]
                        })

                    return {
                        "assets": assets,
                        "findings": [],
                        "metadata": {"tech_count": len(techs)}
                    }
        except Exception as e:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "Tech Detection Error", "description": str(e)}], "metadata": {}}

# Auto-injected Metadata
PLUGIN_NAME = "tech_detection"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for tech_detection"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = ["aiohttp"]

PLUGIN_EXTERNAL_TOOLS = []
