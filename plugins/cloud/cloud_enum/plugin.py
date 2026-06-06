from core.http.client import HttpClient
import aiohttp


class Plugin:
    name = 'cloud_enum'
    category = 'cloud'
    async def run(target: str, context: dict) -> dict -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}
            
        domain = target.replace("http://", "").replace("https://", "").split("/")[0]
        
        # Heuristics for cloud buckets
        buckets_to_check = [
            f"https://{domain}.s3.amazonaws.com",
            f"https://{domain}-assets.s3.amazonaws.com",
            f"https://{domain.replace('.', '-')}.s3.amazonaws.com"
        ]

        assets = []
        findings = []
        
        async with HttpClient() as session:
            for url in buckets_to_check:
                try:
                    async with session.head(url, timeout=5) as resp:
                        if resp.status in [200, 403]:  # 403 means it exists but is private
                            assets.append({
                                "type": "cloud_bucket",
                                "value": url,
                                "tags": ["aws", "s3", "cloud_enum"]
                            })
                            if resp.status == 200:
                                findings.append({
                                    "type": "vulnerability",
                                    "title": "Public S3 Bucket Discovered",
                                    "severity": "high",
                                    "description": f"The AWS S3 bucket {url} is publicly accessible.",
                                    "evidence": url
                                })
                except Exception:
                    pass

        return {
            "assets": assets,
            "findings": findings,
            "metadata": {"cloud_checks": len(buckets_to_check)}
        }
