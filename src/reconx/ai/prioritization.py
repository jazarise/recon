from typing import List


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
