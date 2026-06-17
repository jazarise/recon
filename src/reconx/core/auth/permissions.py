import enum
from reconx.core.auth.roles import Role


class Permission(str, enum.Enum):
    MANAGE_USERS = "manage_users"
    MANAGE_PROJECTS = "manage_projects"
    MANAGE_PLUGINS = "manage_plugins"
    MANAGE_SETTINGS = "manage_settings"

    RUN_SCAN = "run_scan"
    MANAGE_TARGETS = "manage_targets"
    MANAGE_ASSETS = "manage_assets"
    GENERATE_REPORTS = "generate_reports"

    VIEW_PROJECTS = "view_projects"
    VIEW_SCANS = "view_scans"
    VIEW_REPORTS = "view_reports"
    VIEW_FINDINGS = "view_findings"


ROLE_PERMISSIONS = {
    Role.ADMIN: [
        Permission.MANAGE_USERS,
        Permission.MANAGE_PROJECTS,
        Permission.MANAGE_PLUGINS,
        Permission.MANAGE_SETTINGS,
        Permission.RUN_SCAN,
        Permission.MANAGE_TARGETS,
        Permission.MANAGE_ASSETS,
        Permission.GENERATE_REPORTS,
        Permission.VIEW_PROJECTS,
        Permission.VIEW_SCANS,
        Permission.VIEW_REPORTS,
        Permission.VIEW_FINDINGS,
    ],
    Role.OPERATOR: [
        Permission.RUN_SCAN,
        Permission.MANAGE_TARGETS,
        Permission.MANAGE_ASSETS,
        Permission.GENERATE_REPORTS,
        Permission.VIEW_PROJECTS,
        Permission.VIEW_SCANS,
        Permission.VIEW_REPORTS,
        Permission.VIEW_FINDINGS,
    ],
    Role.VIEWER: [
        Permission.VIEW_PROJECTS,
        Permission.VIEW_SCANS,
        Permission.VIEW_REPORTS,
        Permission.VIEW_FINDINGS,
    ],
}


def has_permission(role: str, permission: Permission) -> bool:
    try:
        r = Role(role)
        return permission in ROLE_PERMISSIONS[r]
    except ValueError:
        return False
