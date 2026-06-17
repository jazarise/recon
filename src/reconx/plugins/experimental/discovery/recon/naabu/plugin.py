from reconx.core.plugin_base import standardize_output
import json
import asyncio
import shutil



class Plugin:
    name = 'naabu'
    category = 'recon'
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target")
        if not target:
            raise ValueError("No target provided to naabu plugin")

        naabu_path = shutil.which("naabu")
        if not naabu_path:
            raise FileNotFoundError("naabu binary not found in PATH")

        project_dir = OUTPUTS_DIR / "projects" / target
        input_file = project_dir / "subdomains.txt"
        
        if not input_file.exists():
            input_file = project_dir / "target.txt"
            with open(input_file, "w") as f:
                f.write(f"{target}\n")

        out_file = project_dir / "ports.json"

        # Execute naabu: -l input_file -top-ports 1000 -json -o out_file
        cmd = [
            naabu_path,
            "-l", str(input_file),
            "-top-ports", "1000",
            "-json",
            "-o", str(out_file),
            "-silent"
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0 and process.returncode is not None:
            raise RuntimeError(f"Naabu failed: {stderr.decode()}")

        open_ports = []
        findings = []

        if out_file.exists():
            with open(out_file, "r") as f:
                for line in f:
                    if not line.strip(): continue
                    try:
                        data = json.loads(line)
                        host = data.get("host")
                        port = data.get("port")
                        if host and port:
                            open_ports.append(f"{host}:{port}")
                            findings.append({
                                "type": "open_port",
                                "host": host,
                                "port": port,
                                "source": "naabu"
                            })
                    except json.JSONDecodeError:
                        continue

        return {
            "plugin": "naabu",
            "target": target,
            "open_ports_count": len(open_ports),
            "findings": findings
        }

# Auto-injected Metadata
PLUGIN_NAME = "naabu"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for naabu"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = ["naabu"]
