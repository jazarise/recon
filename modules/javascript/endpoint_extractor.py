import re

class EndpointExtractor:
    def extract(self, js_content: str) -> list:
        """
        Statically analyzes JS content for hidden API endpoints and routes.
        Returns a list of discovered endpoints.
        """
        endpoints = set()
        
        # Regex to find fetch/axios calls and string literals looking like API paths
        # Matches: "/api/v1/users", "https://api.internal/v2/config", etc.
        pattern = r'(?:["\'])(/(?:api|internal|v1|v2|graphql|admin)/[^"\']+)(?:["\'])'
        matches = re.findall(pattern, js_content, re.IGNORECASE)
        
        for match in matches:
            endpoints.add(match)
            
        # Match full URLs hardcoded in JS
        url_pattern = r'(?:["\'])(https?://[a-zA-Z0-9.-]+/(?:api|internal|graphql)[^"\']+)(?:["\'])'
        url_matches = re.findall(url_pattern, js_content, re.IGNORECASE)
        
        for match in url_matches:
            endpoints.add(match)
            
        return list(endpoints)

endpoint_extractor = EndpointExtractor()
