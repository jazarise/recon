from reconx.core.plugin_base import standardize_output
import json
import asyncio
import shutil



class Plugin:
    name = 'content_discovery'
    category = 'recon'
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target")
        if not target:
            raise ValueError("No target provided to content_discovery plugin")

        project_dir = OUTPUTS_DIR / "projects" / target
        input_file = project_dir / "alive_urls.txt"
        
        if not input_file.exists():
            input_file = project_dir / "subdomains.txt"
        if not input_file.exists():
            input_file = project_dir / "target.txt"

        findings = []
        endpoints = set()

        # 1. Katana (Crawling)
        out_katana = project_dir / "katana.json"
        if shutil.which("katana"):
            cmd = ["katana", "-list", str(input_file), "-jsonl", "-o", str(out_katana), "-silent"]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await proc.communicate()
            
            if out_katana.exists():
                with open(out_katana, "r") as f:
                    for line in f:
                        if not line.strip(): continue
                        try:
                            d = json.loads(line)
                            url = d.get("request", {}).get("endpoint")
                            if url:
                                endpoints.add(url)
                        except Exception as e:
                            import logging
                            logging.getLogger("content_discovery").error(f"Error parsing katana JSON: {e}")

        # 2. Waybackurls (Historical)
        out_wayback = project_dir / "wayback.txt"
        if shutil.which("waybackurls"):
            # read input line by line, or we can just cat to waybackurls
            # for safety we just use the first target or if we have subdomains, we might skip to save time or just run it on the base target
            cmd = ["waybackurls", target]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, _ = await proc.communicate()
            for line in stdout.decode().splitlines():
                if line.strip():
                    endpoints.add(line.strip())

        # 3. Feroxbuster (Directory Brute)
        # Feroxbuster is very intensive. We will run it only on the main target or alive urls if few.
        out_ferox = project_dir / "feroxbuster.json"
        if shutil.which("feroxbuster"):
            # just run on target for deep scan
            cmd = ["feroxbuster", "-u", f"https://{target}", "--json", "-o", str(out_ferox), "-q"]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await proc.communicate()
            
            if out_ferox.exists():
                with open(out_ferox, "r") as f:
                    for line in f:
                        if not line.strip(): continue
                        try:
                            d = json.loads(line)
                            url = d.get("url")
                            if url:
                                endpoints.add(url)
                                findings.append({"type": "directory", "url": url, "status": d.get("status")})
                        except Exception as e:
                            import logging
                            logging.getLogger("content_discovery").error(f"Error parsing feroxbuster JSON: {e}")

        # Write endpoints
        out_endpoints = project_dir / "endpoints.txt"
        with open(out_endpoints, "w") as f:
            for ep in sorted(list(endpoints)):
                f.write(f"{ep}\n")

        for ep in endpoints:
            findings.append({"type": "endpoint", "url": ep})

        return {
            "plugin": "content_discovery",
            "target": target,
            "endpoints_found": len(endpoints),
            "findings": findings
        }

# Auto-injected Metadata
PLUGIN_NAME = "content_discovery"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for content_discovery"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = ["katana"]
