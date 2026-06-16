class EnterpriseAuth:
    USERS = {
        "token_orgA_owner": {"tenant_id": "org_1", "role": "Owner"},
        "token_orgA_viewer": {"tenant_id": "org_1", "role": "Viewer"},
        "token_orgB_admin": {"tenant_id": "org_2", "role": "Admin"}
    }

    @classmethod
    def resolve_context(cls, token: str) -> dict:
        if token not in cls.USERS:
            raise ValueError("401 Unauthorized: Invalid SSO/API Token")
        return cls.USERS[token]
