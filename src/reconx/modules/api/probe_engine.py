from core.utils.http_client import HttpClient

class ProbeEngine:
    def __init__(self):
        self.http = HttpClient()

    def probe_endpoint(self, base_url: str, endpoint: str) -> dict:
        """
        Actively tests an endpoint using standard methods to determine its state.
        Returns a dictionary of supported methods and their status codes.
        """
        # Ensure we have an absolute URL
        target = endpoint if endpoint.startswith("http") else f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        print(f"[*] Actively probing API endpoint: {target}")
        
        methods_to_test = ["GET", "POST", "OPTIONS"]
        results = {
            "endpoint": target,
            "methods": {}
        }
        
        for method in methods_to_test:
            resp = self.http.request(method, target)
            if resp:
                results["methods"][method] = resp.get("status_code")
                
        return results

probe_engine = ProbeEngine()
