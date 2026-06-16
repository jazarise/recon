from core.plugin_base import standardize_output
from core.http.client import HttpClient
import os
import json
import asyncio
import shutil
from pathlib import Path



class Plugin:
    name = 'subfinder'
    category = 'recon'
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target")
        if not target:
            raise ValueError("No target provided to subfinder plugin")

        # Check if subfinder is installed
        subfinder_path = shutil.which("subfinder")
        if not subfinder_path:
            raise FileNotFoundError("subfinder binary not found in PATH")

        # Prepare output path
        project_dir = OUTPUTS_DIR / "projects" / target
        project_dir.mkdir(parents=True, exist_ok=True)
        out_file = project_dir / "subdomains.json"

        # Execute subfinder: -d domain -all -silent -json -o out_file
        cmd = [
            subfinder_path,
            "-d", target,
            "-all",
            "-silent",
            "-json",
            "-o", str(out_file)
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0 and process.returncode is not None:
            raise RuntimeError(f"Subfinder failed: {stderr.decode()}")

        subdomains = []
        if out_file.exists():
            with open(out_file, "r") as f:
                for line in f:
                    if not line.strip(): continue
                    try:
                        data = json.loads(line)
                        host = data.get("host")
                        if host:
                            subdomains.append(host)
                    except json.JSONDecodeError:
                        continue

        # Write a flat text file for subsequent tools that need a list of hosts
        hosts_file = project_dir / "subdomains.txt"
        with open(hosts_file, "w") as f:
            for sub in subdomains:
                f.write(f"{sub}\n")

        return {
            "plugin": "subfinder",
            "target": target,
            "subdomains_found": len(subdomains),
            "output_file": str(hosts_file),
            "findings": [
                {
                    "type": "subdomain",
                    "domain": sub,
                    "source": "subfinder"
                } for sub in subdomains
            ]
        }

# Auto-injected Metadata
PLUGIN_NAME = "subfinder"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for subfinder"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = ["subfinder"]
