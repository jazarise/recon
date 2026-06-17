from reconx.core.utils.http_client import HttpClient

class GraphQLEngine:
    def __init__(self):
        self.http = HttpClient()

    def introspect(self, base_url: str) -> dict:
        """Attempts to find a GraphQL endpoint and run an introspection query."""
        graphql_paths = ["/graphql", "/api/graphql", "/v1/graphql"]
        
        # Standard basic introspection query to pull top-level types
        query = {
            "query": """
            query {
                __schema {
                    types {
                        name
                        kind
                    }
                }
            }
            """
        }
        
        for path in graphql_paths:
            target = f"{base_url.rstrip('/')}{path}"
            print(f"[*] Probing for GraphQL Introspection at {target}")
            
            # Send POST with JSON payload
            resp = self.http.post(target, json=query)
            if resp and resp.get("status_code") == 200:
                try:
                    data = resp.get("json") or {}
                    if "data" in data and "__schema" in data["data"]:
                        return {
                            "endpoint": target,
                            "schema": data["data"]["__schema"]
                        }
                except:
                    pass
                    
        return {}

graphql_engine = GraphQLEngine()
