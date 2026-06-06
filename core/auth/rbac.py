from enum import Enum

class Role(Enum):
    ADMIN = "Administrator"
    ANALYST = "Analyst"
    OPERATOR = "Operator"
    VIEWER = "Viewer"

class Permission(Enum):
    VIEW = "View"
    EXECUTE = "Execute"
    MODIFY = "Modify"
    DELETE = "Delete"

class User:
    def __init__(self, username: str, role: Role):
        self.username = username
        self.role = role

def check_permission(user: User, perm: Permission) -> bool:
    if user.role == Role.ADMIN: return True
    if perm == Permission.VIEW: return True
    if user.role == Role.OPERATOR and perm in [Permission.EXECUTE, Permission.MODIFY]: return True
    if user.role == Role.ANALYST and perm in [Permission.EXECUTE]: return True
    return False
