class RBACLayer:
    API_KEYS = {
        "rex_admin_999": {"role": "admin", "scopes": ["scan:run", "results:read", "campaign:delete"]},
        "rex_analyst_123": {"role": "analyst", "scopes": ["scan:run", "results:read"]},
        "rex_viewer_000": {"role": "viewer", "scopes": ["results:read"]}
    }

    @classmethod
    def validate_key(cls, token: str, required_scope: str) -> bool:
        if token not in cls.API_KEYS:
            return False
        
        user_scopes = cls.API_KEYS[token]["scopes"]
        if required_scope not in user_scopes and "admin" != cls.API_KEYS[token]["role"]:
            return False
            
        return True
