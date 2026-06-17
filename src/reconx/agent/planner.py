class PlannerAgent:
    def generate_plan(self, goal: str) -> list:
        if goal == "Find admin panels":
            return [
                "Passive DNS collection",
                "Subdomain discovery (high confidence sources)",
                "Filter live hosts",
                "Deep scan only high-risk endpoints",
            ]
        return ["Default wide scan"]
