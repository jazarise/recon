from reconx.core.database.repositories.base import BaseRepository
from reconx.core.database.models import AuditLog


class AuditLogRepository(BaseRepository[AuditLog]):
    pass


audit_log_repo = AuditLogRepository(AuditLog)
