from reconx.core.plugin_base import standardize_output
import urllib.request
import ssl


class Plugin:
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target", "localhost")
        findings = []
        urls = []
        technologies = []
        
        # If network_discovery found ports 80/443, we'll try those. Otherwise default to 80/443.
        ports = [80, 443]
        if "network_discovery" in context and context["network_discovery"]:
            discovered = context["network_discovery"].get("open_ports", [])
            ports = [p for p in discovered if p in (80, 443, 8080, 8443)] or ports

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        for port in ports:
            scheme = "https" if port in (443, 8443) else "http"
            url = f"{scheme}://{target}:{port}"
            if port == 80 and scheme == "http":
                url = f"http://{target}"
            elif port == 443 and scheme == "https":
                url = f"https://{target}"
                
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'ReconX-WebRecon'})
                with urllib.request.urlopen(req, timeout=3, context=ctx) as response:
                    urls.append(url)
                    headers = dict(response.headers)
                    server = headers.get("Server", "Unknown")
                    if server != "Unknown":
                        technologies.append(server)
                        
                    findings.append({
                        "type": "web_service",
                        "url": url,
                        "status": response.status,
                        "server": server
                    })
            except Exception as e:
                findings.append({
                    "type": "web_error",
                    "url": url,
                    "error": str(e)
                })

        return {
            "plugin": "web_recon",
            "urls": urls,
            "technologies": list(set(technologies)),
            "findings": findings
        }

# Auto-injected Metadata
PLUGIN_NAME = "web_recon"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for web_recon"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = []
