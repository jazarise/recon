from core.http.client import HttpClient
import aiohttp


class Plugin:
    name = 'contacts'
    category = 'osint'
    async def get_hunter_contacts(self, domain: str) -> list:
        # Replaces recon-ng's contacts/hunter module
        # Note: In a real environment, this requires an API key in config
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&limit=10"
        try:
            async with HttpClient() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("data", {}).get("emails", [])
        except Exception as e:
            return [{"error": str(e)}]
        return []

    async def run(target: str, context: dict) -> dict -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}

        emails = await self.get_hunter_contacts(target)
        
        assets = []
        findings = []

        if emails and "error" in emails[0]:
            findings.append({"type": "error", "severity": "info", "title": "Contacts API Error", "description": emails[0]["error"]})
        else:
            for em in emails:
                val = em if isinstance(em, str) else em.get("value")
                if val:
                    assets.append({
                        "type": "email",
                        "value": val,
                        "tags": ["osint", "recon-ng", "contact"]
                    })

        return {
            "assets": assets,
            "findings": findings,
            "metadata": {"contacts_count": len(assets)}
        }
