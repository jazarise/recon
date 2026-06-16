class HeuristicsEngine:
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
