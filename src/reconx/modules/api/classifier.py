class APIClassifier:
    def classify(self, probe_results: dict) -> str:
        """
        Analyzes the HTTP status codes from the probe engine to classify the API endpoint.
        Returns classifications like PUBLIC, AUTHENTICATED, FORBIDDEN.
        """
        methods = probe_results.get("methods", {})
        
        # If any method returns 200/201, it's public
        if any(code in [200, 201, 204] for code in methods.values()):
            return "PUBLIC"
            
        # If it explicitly returns 401, it requires auth
        if any(code == 401 for code in methods.values()):
            return "AUTHENTICATED"
            
        # If it returns 403, it's forbidden/admin restricted
        if any(code == 403 for code in methods.values()):
            return "ADMIN/FORBIDDEN"
            
        return "UNKNOWN"

api_classifier = APIClassifier()
