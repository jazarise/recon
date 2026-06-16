from core.models import Asset, AssetType

class AssetNormalizer:
    @staticmethod
    def create_subdomain(value: str, source: str) -> Asset:
        return Asset(type=AssetType.SUBDOMAIN, value=value, source=source)

    @staticmethod
    def create_url(value: str, source: str) -> Asset:
        return Asset(type=AssetType.URL, value=value, source=source)

    @staticmethod
    def create_ip(value: str, source: str) -> Asset:
        return Asset(type=AssetType.IP, value=value, source=source)
