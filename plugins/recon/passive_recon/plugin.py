from core.http.client import HttpClient
import os
import asyncio
import shutil
from pathlib import Path



class Plugin:
    name = 'passive_recon'
    category = 'recon'
    async def run(target: str, context: dict) -> dict -> dict:
        target = context.get("target")
        if not target:
            raise ValueError("No target provided to passive_recon plugin")

        project_dir = OUTPUTS_DIR / "projects" / target
        project_dir.mkdir(parents=True, exist_ok=True)
        
        out_subfinder = project_dir / "subfinder.txt"
        out_assetfinder = project_dir / "assetfinder.txt"
        final_subs = project_dir / "subdomains.txt"

        subdomains = set()

        # Run Subfinder
        if shutil.which("subfinder"):
            cmd = ["subfinder", "-d", target, "-all", "-silent", "-o", str(out_subfinder)]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await proc.communicate()
            if out_subfinder.exists():
                with open(out_subfinder, "r") as f:
                    for line in f:
                        if line.strip(): subdomains.add(line.strip())
        
        # Run Assetfinder
        if shutil.which("assetfinder"):
            cmd = ["assetfinder", "--subs-only", target]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, _ = await proc.communicate()
            for line in stdout.decode().splitlines():
                if line.strip(): subdomains.add(line.strip())

        # Write merged subdomains
        with open(final_subs, "w") as f:
            for sub in sorted(list(subdomains)):
                f.write(f"{sub}\n")

        return {
            "plugin": "passive_recon",
            "target": target,
            "subdomains_found": len(subdomains),
            "output_file": str(final_subs),
            "findings": [
                {"type": "subdomain", "domain": sub, "source": "passive_recon"}
                for sub in subdomains
            ]
        }
