class EnrichmentEngine:
    async def enrich_asset(self, asset: dict) -> dict:
        # Interface design only, no hardcoded providers.
        # Future sources: WHOIS, ASN, DNS, TLS, Technology Detection
        return asset
