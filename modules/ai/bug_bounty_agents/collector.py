import os
from pathlib import Path
from core.models import Finding

class BugBountyAgentsCollector:
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"

    def collect(self, target: str, **kwargs) -> list:
        findings = []
        if not self.data_dir.exists():
            return findings
            
        for file in self.data_dir.glob("*.md"):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                finding = Finding(
                    category="ai_agent_prompt",
                    source="bug_bounty_agents",
                    value=content,
                    metadata={"agent_name": file.stem}
                )
                findings.append(finding)
        return findings
