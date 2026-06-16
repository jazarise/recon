import subprocess

TOOLS = {
    "subfinder": {
        "version": "latest",
        "type": "external",
        "capabilities": ["discovery.subdomains"]
    },
    "amass": {
        "version": "latest",
        "type": "external",
        "capabilities": ["discovery.subdomains"]
    },
    "assetfinder": {
        "version": "latest",
        "type": "external",
        "capabilities": ["discovery.subdomains"]
    },
    "katana": {
        "version": "latest",
        "type": "external",
        "capabilities": ["content.crawl"]
    },
    "dalfox": {
        "version": "latest",
        "type": "external",
        "capabilities": ["vuln.xss"]
    },
    "nuclei": {
        "version": "latest",
        "type": "external",
        "capabilities": ["vuln.templates"]
    }
}

class ToolRegistry:
    def __init__(self):
        self.tools = TOOLS
        
    def check_tool_installed(self, tool_name: str) -> bool:
        """Check if an external tool is available in the system PATH."""
        try:
            # For Windows we might need to check if the executable is available.
            # A simple approach is using 'where' on Windows or 'which' on Unix.
            import os
            cmd = "where" if os.name == "nt" else "which"
            result = subprocess.run([cmd, tool_name], capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

tool_registry = ToolRegistry()
