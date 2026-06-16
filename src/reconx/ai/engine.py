from src.reconx.ai.heuristics import HeuristicsEngine
from src.reconx.ai.graph import AttackGraph
from src.reconx.ai.memory import ContextMemory
from src.reconx.ai.prioritization import PrioritizationEngine

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
