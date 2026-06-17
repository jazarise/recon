from reconx.core.plugin_base import standardize_output
from reconx.core.http.client import HttpClient
from bs4 import BeautifulSoup


class Plugin:
    name = 'metadata'
    category = 'osint'
    async def extract_metadata(self, url: str) -> dict:
        # Replaces recon-ng's metadata extraction module (e.g. title, descriptions)
        if not url.startswith("http"):
            url = "https://" + url
            
        try:
            async with HttpClient() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        soup = BeautifulSoup(text, 'html.parser')
                        title = soup.title.string if soup.title else ""
                        desc = soup.find('meta', attrs={'name': 'description'})
                        desc = desc['content'] if desc else ""
                        return {"title": title, "description": desc}
        except Exception as e:
            return {"error": str(e)}
        return {}

    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}

        meta = await self.extract_metadata(target)
        
        assets = []
        findings = []

        if "error" in meta:
            findings.append({"type": "error", "severity": "info", "title": "Metadata API Error", "description": meta["error"]})
        else:
            if meta.get("title"):
                assets.append({"type": "metadata", "value": meta["title"], "tags": ["osint", "title"]})
            if meta.get("description"):
                assets.append({"type": "metadata", "value": meta["description"], "tags": ["osint", "description"]})

        return {
            "assets": assets,
            "findings": findings,
            "metadata": {"extracted": True}
        }

# Auto-injected Metadata
PLUGIN_NAME = "metadata"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "OSINT"
PLUGIN_DESCRIPTION = "Auto-generated description for metadata"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["osint"]

PLUGIN_DEPENDENCIES = ["beautifulsoup4", "aiohttp"]

PLUGIN_EXTERNAL_TOOLS = []
