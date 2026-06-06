from core.http.client import HttpClient
import os
import json
import asyncio
import shutil
from pathlib import Path



class Plugin:
    name = 'active_recon'
    category = 'recon'
    async def run(target: str, context: dict) -> dict -> dict:
        target = context.get("target")
        if not target:
            raise ValueError("No target provided to active_recon plugin")

        project_dir = OUTPUTS_DIR / "projects" / target
        input_file = project_dir / "subdomains.txt"
        
        if not input_file.exists():
            input_file = project_dir / "target.txt"
            with open(input_file, "w") as f:
                f.write(f"{target}\n")

        # 1. DNSX
        out_dnsx = project_dir / "dnsx.json"
        if shutil.which("dnsx"):
            cmd = ["dnsx", "-l", str(input_file), "-a", "-cname", "-json", "-o", str(out_dnsx), "-silent"]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await proc.communicate()

        # 2. HTTPX
        out_httpx = project_dir / "httpx.json"
        alive_urls = project_dir / "alive_urls.txt"
        if shutil.which("httpx"):
            cmd = ["httpx", "-l", str(input_file), "-title", "-tech-detect", "-status-code", "-json", "-o", str(out_httpx), "-silent"]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await proc.communicate()
            
            # Extract alive urls
            urls = []
            if out_httpx.exists():
                with open(out_httpx, "r") as f:
                    for line in f:
                        if not line.strip(): continue
                        try:
                            d = json.loads(line)
                            if d.get("url"): urls.append(d["url"])
                        except Exception as e:
                            import logging
                            logging.getLogger("active_recon").error(f"Error parsing httpx JSON: {e}")
            with open(alive_urls, "w") as f:
                for u in urls: f.write(f"{u}\n")

        # 3. NAABU
        out_naabu = project_dir / "ports.json"
        if shutil.which("naabu"):
            cmd = ["naabu", "-l", str(input_file), "-top-ports", "1000", "-json", "-o", str(out_naabu), "-silent"]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await proc.communicate()

        # Build findings payload
        findings = []
        
        # Parse dnsx
        if out_dnsx.exists():
            with open(out_dnsx, "r") as f:
                for line in f:
                    try:
                        d = json.loads(line)
                        findings.append({"type": "dns", "host": d.get("host"), "a": d.get("a"), "cname": d.get("cname")})
                    except Exception as e:
                        import logging
                        logging.getLogger("active_recon").error(f"Error parsing dnsx JSON: {e}")

        # Parse httpx
        if out_httpx.exists():
            with open(out_httpx, "r") as f:
                for line in f:
                    try:
                        d = json.loads(line)
                        findings.append({
                            "type": "web_host",
                            "url": d.get("url"),
                            "status_code": d.get("status_code"),
                            "title": d.get("title"),
                            "technologies": d.get("tech", [])
                        })
                    except Exception as e:
                        import logging
                        logging.getLogger("active_recon").error(f"Error parsing httpx JSON: {e}")

        # Parse naabu
        if out_naabu.exists():
            with open(out_naabu, "r") as f:
                for line in f:
                    try:
                        d = json.loads(line)
                        findings.append({"type": "open_port", "host": d.get("host"), "port": d.get("port")})
                    except Exception as e:
                        import logging
                        logging.getLogger("active_recon").error(f"Error parsing naabu JSON: {e}")

        return {
            "plugin": "active_recon",
            "target": target,
            "findings": findings
        }
