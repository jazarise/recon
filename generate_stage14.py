import os

files = {
    "config.yaml": """threads: 20
timeout: 5
retries: 3
output_format: json
plugins_enabled:
  - dns_enum
  - subdomain_enum
  - port_scan
  - tech_detect
stealth:
  enabled: false
  jitter_range: [0.2, 1.5]
  max_requests_per_second: 2
  passive_only: true
  user_agent_rotation: true
  proxy_enabled: false
ai_engine:
  enabled: true
  prioritization: true
  attack_graph: true
  noise_filtering: true
  suggestion_mode: active
""",
    "src/reconx/ai/heuristics.py": """class HeuristicsEngine:
    HIGH_RISK_KEYWORDS = ["admin", "login", "api", "dashboard", "portal"]
    LOW_RISK_KEYWORDS = ["cdn", "static", "assets", "fonts", "css"]

    @classmethod
    def evaluate_subdomain(cls, subdomain: str) -> str:
        for keyword in cls.HIGH_RISK_KEYWORDS:
            if keyword in subdomain:
                return "HIGH"
        for keyword in cls.LOW_RISK_KEYWORDS:
            if keyword in subdomain:
                return "LOW"
        return "MEDIUM"

    @classmethod
    def evaluate_service(cls, port: int, tech: list) -> str:
        if port in [22, 3389]:
            return "HIGH (Exposed Remote Access)"
        if port in [80, 443] and any("PHP" in t for t in tech):
            return "MEDIUM (Legacy Web Stack)"
        return "LOW"
""",
    "src/reconx/ai/graph.py": """import json

class AttackGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_relationship(self, source: str, target: str):
        self.nodes.add(source)
        self.nodes.add(target)
        self.edges.add(f"{source} -> {target}")

    def export(self):
        return {
            "nodes": list(self.nodes),
            "edges": list(self.edges)
        }
""",
    "src/reconx/ai/memory.py": """class ContextMemory:
    def __init__(self):
        self._scanned = set()
        self._failed = set()

    def mark_scanned(self, target: str):
        self._scanned.add(target)

    def mark_failed(self, target: str):
        self._failed.add(target)

    def should_scan(self, target: str) -> bool:
        if target in self._scanned or target in self._failed:
            return False
        return True
""",
    "src/reconx/ai/prioritization.py": """from typing import List, Dict

class PrioritizationEngine:
    @staticmethod
    def generate_next_actions(high_risk_targets: List[str]) -> List[str]:
        actions = []
        for target in high_risk_targets:
            if "api" in target:
                actions.append(f"Enumerate API routes on {target}")
            elif "admin" in target or "login" in target:
                actions.append(f"Test authentication bypass on {target}")
            else:
                actions.append(f"Run deep port scan on high-value asset {target}")
        return actions
""",
    "src/reconx/ai/engine.py": '''from reconx.ai.heuristics import HeuristicsEngine
from reconx.ai.graph import AttackGraph
from reconx.ai.memory import ContextMemory
from reconx.ai.prioritization import PrioritizationEngine

class IntelligenceEngine:
    def __init__(self):
        self.memory = ContextMemory()
        self.graph = AttackGraph()

    def process_raw_data(self, target: str, data: dict) -> dict:
        """Transforms raw output into structured intelligence."""
        report = {
            "target": target,
            "attack_surface": {
                "high_risk": [],
                "medium_risk": [],
                "low_risk": []
            },
            "recommendations": []
        }

        # Subdomain Evaluation
        for sub in data.get("subdomains", []):
            self.graph.add_relationship(target, sub)
            risk = HeuristicsEngine.evaluate_subdomain(sub)
            if risk == "HIGH":
                report["attack_surface"]["high_risk"].append(sub)
            elif risk == "LOW":
                report["attack_surface"]["low_risk"].append(sub)
            else:
                report["attack_surface"]["medium_risk"].append(sub)

        # Service Evaluation
        for port in data.get("ports", []):
            risk_label = HeuristicsEngine.evaluate_service(port, data.get("tech_stack", []))
            if "HIGH" in risk_label:
                report["attack_surface"]["high_risk"].append(f"Port {port}")

        # Next Best Actions
        report["recommendations"] = PrioritizationEngine.generate_next_actions(
            report["attack_surface"]["high_risk"]
        )

        return report
''',
    "src/reconx/reporting/ai_exporter.py": '''import json

def export_intelligence_report(report_data: dict, filepath: str):
    """Outputs the structured AI reasoning report."""
    with open(filepath, 'w') as f:
        f.write(f"TARGET: {report_data['target']}\\n\\n")
        
        f.write("ATTACK SURFACE SUMMARY:\\n")
        f.write(f"- High-risk endpoints: {len(report_data['attack_surface']['high_risk'])}\\n")
        f.write(f"- Medium-risk endpoints: {len(report_data['attack_surface']['medium_risk'])}\\n")
        f.write(f"- Low-risk noise (Ignored): {len(report_data['attack_surface']['low_risk'])}\\n\\n")
        
        f.write("PRIORITY TARGETS:\\n")
        for idx, t in enumerate(report_data['attack_surface']['high_risk']):
            f.write(f"{idx+1}. {t} (HIGH)\\n")
            
        f.write("\\nRECOMMENDED NEXT ACTIONS:\\n")
        for action in report_data['recommendations']:
            f.write(f"- {action}\\n")
''',
    "tests/test_ai_engine.py": """def test_ai_prioritization():
    from reconx.ai.engine import IntelligenceEngine
    
    engine = IntelligenceEngine()
    
    mock_data = {
        "subdomains": ["admin.example.com", "cdn.example.com", "www.example.com"],
        "ports": [80, 22],
        "tech_stack": ["nginx"]
    }
    
    result = engine.process_raw_data("example.com", mock_data)
    
    assert "admin.example.com" in result["attack_surface"]["high_risk"]
    assert "cdn.example.com" in result["attack_surface"]["low_risk"]
    assert "Port 22" in result["attack_surface"]["high_risk"]
    assert len(result["recommendations"]) >= 2
""",
    "docs/reports/stage14_ai_engine.md": """# Stage 14: AI Engine Architecture

## Heuristics Filtering
We implemented `src/reconx/ai/heuristics.py` to natively classify discovered vectors. Subdomains with keywords like `admin` or `api` are auto-elevated to HIGH, while `cdn` or `static` nodes are demoted to LOW noise.

## Attack Path Graph
The `AttackGraph` module locally tracks nodes mapping DNS relationships (e.g., `example.com -> admin.example.com`), allowing us to visualize structural pivots.

## Next-Best Action Prioritization
Instead of blindly dumping `Port 22` open logs, the `PrioritizationEngine` generates actionable plain-text output in the `ai_exporter.py` recommending specific actions like *"Test authentication bypass on admin.example.com"*.
""",
}

for path, content in files.items():
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
