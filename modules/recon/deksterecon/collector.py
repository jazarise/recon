import subprocess
from core.models import Finding
from typing import List

class DekstereconCollector:
    def __init__(self):
        self.tools = {
            "amass": ["amass", "enum", "-d"],
            "assetfinder": ["assetfinder", "--subs-only"],
            "subfinder": ["subfinder", "-d"],
            "findomain": ["findomain", "-t"],
            "httpx": ["httpx", "-u"],
            "waybackurls": ["waybackurls"]
        }

    def _run_tool(self, name: str, command: List[str], target: str) -> str:
        cmd = command.copy()
        if name == "waybackurls":
            # Some tools pipe from stdin or take arguments differently, but basic form:
            cmd = ['echo', target, '|', 'waybackurls']
            # We mock the echo | waybackurls by running waybackurls directly and passing target as input
            try:
                result = subprocess.run(["waybackurls"], input=target, capture_output=True, text=True, timeout=120)
                return result.stdout.strip()
            except FileNotFoundError:
                return f"[!] Tool not found: waybackurls"
            except Exception as e:
                return f"[!] Error running waybackurls: {e}"
        else:
            cmd.append(target)
            
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            out = result.stdout.strip()
            err = result.stderr.strip()
            if out: return out
            if err: return err
            return "[!] No output"
        except FileNotFoundError:
            return f"[!] Tool not found: {cmd[0]}"
        except Exception as e:
            return f"[!] Error running {cmd[0]}: {e}"

    def collect(self, target: str, **kwargs) -> list:
        findings = []
        for name, cmd in self.tools.items():
            output = self._run_tool(name, cmd, target)
            finding = Finding(
                category="deksterecon_result",
                source="deksterecon",
                value=output,
                metadata={"tool": name, "target": target}
            )
            findings.append(finding)
        return findings
