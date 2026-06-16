from core.models.enums import AssetType

class MitreMapper:
    """Translates generic asset findings into standardized MITRE ATT&CK techniques."""
    
    def __init__(self):
        # Heuristic rules mapping Asset -> MITRE Technique
        self.rules = {
            "API_MISSING_AUTH": {
                "id": "T1190",
                "name": "Exploit Public-Facing Application",
                "description": "Unauthenticated API endpoints can be directly exploited to access internal functions."
            },
            "EXPOSED_SECRET": {
                "id": "T1552.001",
                "name": "Unsecured Credentials: Local Accounts",
                "description": "Hardcoded AWS keys or JWTs found in client-side code."
            },
            "OPENAPI_LEAK": {
                "id": "T1592.002",
                "name": "Gather Victim Host Information: Software",
                "description": "Swagger documentation reveals internal API structures and versioning."
            }
        }
        
    def map_asset_to_technique(self, asset_type: AssetType, value: str, context: dict = None) -> dict:
        """Returns the MITRE Technique dict if a heuristic matches, else None."""
        context = context or {}
        
        if asset_type == AssetType.API_ENDPOINT and context.get("auth") == "PUBLIC":
            return self.rules["API_MISSING_AUTH"]
            
        if asset_type == AssetType.SECRET:
            return self.rules["EXPOSED_SECRET"]
            
        if asset_type == AssetType.OPENAPI_SPEC:
            return self.rules["OPENAPI_LEAK"]
            
        return None

mitre_mapper = MitreMapper()
