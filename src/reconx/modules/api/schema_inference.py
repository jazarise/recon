from reconx.core.utils.http_client import HttpClient

class SchemaInferenceEngine:
    def __init__(self):
        self.http = HttpClient()

    def discover_openapi(self, base_url: str) -> dict:
        """Probes for standard Swagger/OpenAPI documentation files."""
        swagger_paths = [
            "/swagger.json",
            "/openapi.json",
            "/api-docs",
            "/docs",
            "/v3/api-docs"
        ]
        
        for path in swagger_paths:
            target = f"{base_url.rstrip('/')}{path}"
            print(f"[*] Probing for OpenAPI spec at {target}")
            
            resp = self.http.get(target)
            if resp and resp.get("status_code") == 200:
                try:
                    import json
                    data = json.loads(resp.get("text"))
                    # Basic heuristic for Swagger/OpenAPI spec
                    if "swagger" in data or "openapi" in data or "paths" in data:
                        return {
                            "endpoint": target,
                            "spec": data
                        }
                except:
                    pass
                    
        return {}

schema_inference_engine = SchemaInferenceEngine()
