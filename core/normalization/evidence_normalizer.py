from core.models import Evidence
from typing import Any

class EvidenceNormalizer:
    @staticmethod
    def capture(source: str, raw_output: Any) -> Evidence:
        return Evidence(
            source=source,
            raw_output=raw_output
        )
