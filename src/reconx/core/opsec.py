from enum import Enum
import logging

logger = logging.getLogger("reconx")

class RiskScore(Enum):
    LOW = 1     # Passive DNS, WHOIS
    MEDIUM = 2  # Light HTTP Probing
    HIGH = 3    # Active Port Scanning / Fuzzing

class DetectionEngine:
    """Evaluates plugin risk against current execution mode."""
    def __init__(self, mode: str):
        self.mode = mode

    def should_execute(self, plugin_name: str, risk: RiskScore) -> bool:
        if self.mode == "stealth" and risk == RiskScore.HIGH:
            logger.warning(f"OPSEC BLOCK: Suppressing {plugin_name} (HIGH RISK) in stealth mode.")
            return False
        return True
