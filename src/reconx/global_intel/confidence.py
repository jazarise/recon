import logging

logger = logging.getLogger("reconx")

class NoiseController:
    @staticmethod
    def assign_confidence(source: str, asset: str) -> str:
        verified_sources = ["cert_transparency", "active_dns"]
        if source in verified_sources:
            return "High"
        if "osint" in source:
            return "Low"
        return "Medium"

    @classmethod
    def filter_noise(cls, source: str, asset: str) -> bool:
        if cls.assign_confidence(source, asset) == "Low":
            logger.debug(f"[NOISE SUPPRESSION] Dropped unverified OSINT signal for {asset}")
            return False
        return True
