import json
from pathlib import Path
from core.models import Finding

class CyberDeckCollector:
    def __init__(self):
        self.data_file = Path(__file__).parent / "data" / "commands.json"
        
    def load_commands(self) -> list:
        if not self.data_file.exists():
            return []
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('commands', [])

    def collect(self, target: str, **kwargs) -> list:
        commands = self.load_commands()
        
        findings = []
        for cmd in commands:
            name = cmd.get('Name', 'Unknown')
            command_str = cmd.get('Command', '')
            os_target = cmd.get('OS', 'Any')
            
            value = f"[{name}] (OS: {os_target}) -> {command_str}"
            
            finding = Finding(
                category="cyberdeck_command",
                source="cyberdeck",
                value=value,
                metadata={"confidence": "high", "severity": "info", "target_os": os_target}
            )
            findings.append(finding)
            
        return findings
