class Plugin:
    name = "dns_enum"

    async def run(self, target: str):
        # Simulated DNS query
        return {"subdomains": [f"www.{target}", f"api.{target}"]}
