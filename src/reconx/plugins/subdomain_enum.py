class Plugin:
    name = "subdomain_enum"

    async def run(self, target: str):
        # Simulated Subdomain scan
        return {"subdomains": [f"dev.{target}", f"staging.{target}"]}
