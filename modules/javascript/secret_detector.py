import re

class SecretDetector:
    def detect(self, js_content: str) -> list:
        """
        Scans JS content for hardcoded secrets, API keys, and JWTs.
        Returns a list of dicts: [{"type": "AWS_KEY", "value": "..."}]
        """
        secrets = []
        
        # AWS Keys
        aws_pattern = r'(AKIA[0-9A-Z]{16})'
        aws_matches = re.findall(aws_pattern, js_content)
        for match in set(aws_matches):
            secrets.append({"type": "AWS_KEY", "value": match})
            
        # Google API Keys
        gcp_pattern = r'(AIza[0-9A-Za-z-_]{35})'
        gcp_matches = re.findall(gcp_pattern, js_content)
        for match in set(gcp_matches):
            secrets.append({"type": "GCP_KEY", "value": match})
            
        # JWT Tokens
        jwt_pattern = r'(eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)'
        jwt_matches = re.findall(jwt_pattern, js_content)
        for match in set(jwt_matches):
            secrets.append({"type": "JWT", "value": match})
            
        return secrets

secret_detector = SecretDetector()
