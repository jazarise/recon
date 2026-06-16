from reconx.core.models import Finding, Severity

class FindingNormalizer:
    @staticmethod
    def create_finding(title: str, severity: Severity, capability: str, source: str, asset_id: str = None) -> Finding:
        return Finding(
            title=title,
            severity=severity,
            asset_id=asset_id,
            capability=capability,
            source=source
        )
