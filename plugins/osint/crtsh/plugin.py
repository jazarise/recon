from core.plugin_base import standardize_output
from core.http.client import HttpClient
import aiohttp


class Plugin:
    name = 'crtsh'
    category = 'osint'
    async def query_crtsh(self, domain: str) -> list:
        # Replaces recon-ng's recon/domains-hosts/certificate_transparency module
        url = f"https://crt.sh/?q={domain}&output=json"
        try:
            async with HttpClient() as session:
                async with session.get(url, timeout=15) as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception as e:
            return [{"error": str(e)}]
        return []

    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}

        data = await self.query_crtsh(target)
        
        assets = []
        findings = []
        metadata = {}

        if data and isinstance(data, list) and "error" in data[0]:
            findings.append({"type": "error", "severity": "info", "title": "crt.sh Error", "description": data[0]["error"]})
        else:
            unique_domains = set()
            for entry in data:
                name_value = entry.get("name_value", "")
                for d in name_value.split("\n"):
                    d = d.strip().lower()
                    if d.endswith(target) and "*" not in d:
                        unique_domains.add(d)

            for d in unique_domains:
                assets.append({
                    "type": "subdomain",
                    "value": d,
                    "tags": ["recon-ng", "crtsh", "osint"]
                })
            
            metadata["crtsh_count"] = len(unique_domains)

        return {
            "assets": assets,
            "findings": findings,
            "metadata": metadata
        }

# Auto-injected Metadata
PLUGIN_NAME = "crtsh"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "OSINT"
PLUGIN_DESCRIPTION = "Auto-generated description for crtsh"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["osint"]

PLUGIN_DEPENDENCIES = ["aiohttp"]

PLUGIN_EXTERNAL_TOOLS = []
