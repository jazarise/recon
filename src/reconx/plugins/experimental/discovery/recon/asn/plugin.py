from reconx.core.plugin_base import standardize_output
from reconx.core.http.client import HttpClient


class Plugin:
    name = 'asn'
    category = 'recon'
    async def get_asn_info(self, query: str) -> dict:
        # Replaces metabigor's ASN discovery using bgpview API natively in Python
        url = f"https://api.bgpview.io/search?query_term={query}"
        try:
            async with HttpClient() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("data", {})
        except Exception as e:
            return {"error": str(e)}
        return {}

    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}

        asn_data = await self.get_asn_info(target)
        
        assets = []
        findings = []
        metadata = {}

        if "error" in asn_data:
            findings.append({"type": "error", "severity": "info", "title": "BGPView Error", "description": asn_data["error"]})
        else:
            # Parse IPv4 prefixes
            ipv4_prefixes = asn_data.get("ipv4_prefixes", [])
            for prefix in ipv4_prefixes:
                assets.append({
                    "type": "cidr",
                    "value": prefix.get("prefix"),
                    "tags": ["asn", "metabigor", prefix.get("name", "")]
                })
            
            # Parse ASNs
            asns = asn_data.get("asns", [])
            for asn in asns:
                asn_code = asn.get("asn")
                assets.append({
                    "type": "asn",
                    "value": f"AS{asn_code}",
                    "tags": ["metabigor", asn.get("name", "")]
                })
            
            metadata["bgpview_raw"] = asn_data

        return {
            "assets": assets,
            "findings": findings,
            "metadata": metadata
        }

# Auto-injected Metadata
PLUGIN_NAME = "asn"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for asn"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = ["aiohttp"]

PLUGIN_EXTERNAL_TOOLS = []
