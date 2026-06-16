import uuid

class Organization:
    def __init__(self, name: str, plan: str):
        self.tenant_id = str(uuid.uuid4())
        self.name = name
        self.plan = plan # Free, Pro, Enterprise
        self.users = []
        self.projects = []

class TenantContext:
    _current_tenant = None

    @classmethod
    def set_tenant(cls, tenant_id: str):
        cls._current_tenant = tenant_id

    @classmethod
    def get_tenant(cls) -> str:
        if not cls._current_tenant:
            raise PermissionError("CRITICAL: No active Tenant ID isolated in current execution context.")
        return cls._current_tenant
