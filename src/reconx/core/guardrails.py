class ScopeEnforcer:
    ALLOWED_SCOPES = [".example.com", "scanme.nmap.org"]

    @classmethod
    def validate_target(cls, target: str) -> bool:
        for scope in cls.ALLOWED_SCOPES:
            if target.endswith(scope) or target == scope:
                return True
        return False
