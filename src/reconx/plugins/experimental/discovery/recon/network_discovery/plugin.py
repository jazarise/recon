from core.plugin_base import standardize_output
from core.http.client import HttpClient
import asyncio
import time


class Plugin:
    name = 'network_discovery'
    category = 'recon'
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target", "localhost")
        ports_to_scan = config.get("ports", [80, 443, 22, 21, 3306])
        open_ports = []
        services = []
        
        start_time = time.time()
        
        async def check_port(port):
            try:
                conn = asyncio.open_connection(target, port)
                reader, writer = await asyncio.wait_for(conn, timeout=1.0)
                open_ports.append(port)
                services.append({"port": port, "state": "open"})
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

        await asyncio.gather(*(check_port(p) for p in ports_to_scan))
        
        return {
            "plugin": "network_discovery",
            "hosts": [target],
            "services": services,
            "open_ports": open_ports,
            "execution_time": round(time.time() - start_time, 2),
            "findings": [
                {
                    "type": "open_port",
                    "port": p,
                    "target": target
                } for p in open_ports
            ]
        }

# Auto-injected Metadata
PLUGIN_NAME = "network_discovery"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for network_discovery"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = []
