
ROLE_HIERARCHY = {
    "ADMIN": 100,
    "ANALYST": 50,
    "VIEWER": 10
}

def has_permission(user_role: str, required_role: str) -> bool:
    user_level = ROLE_HIERARCHY.get(user_role, 0)
    required_level = ROLE_HIERARCHY.get(required_role, 100)
    return user_level >= required_level

class PermissionDeniedError(Exception):
    pass
