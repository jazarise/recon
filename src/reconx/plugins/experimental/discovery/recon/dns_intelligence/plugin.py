from reconx.core.plugin_base import standardize_output
import socket
import asyncio


class Plugin:
    name = 'dns_intelligence'
    category = 'recon'
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target", "localhost")
        findings = []
        records = {}
        subdomains = []
        
        try:
            # Simulate async DNS resolution
            loop = asyncio.get_running_loop()
            hostname, aliases, ips = await loop.run_in_executor(
                None, socket.gethostbyname_ex, target
            )
            
            records["A"] = ips
            if aliases:
                records["CNAME"] = aliases
                
            for ip in ips:
                findings.append({
                    "type": "dns_a_record",
                    "domain": target,
                    "ip": ip
                })
        except Exception as e:
            findings.append({
                "type": "dns_error",
                "domain": target,
                "error": str(e)
            })

        return {
            "plugin": "dns_intelligence",
            "records": records,
            "subdomains": subdomains,
            "findings": findings
        }

# Auto-injected Metadata
PLUGIN_NAME = "dns_intelligence"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for dns_intelligence"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = []
