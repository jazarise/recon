from sqlalchemy.ext.asyncio import AsyncSession
from reconx.core.database.repositories.audit_log import audit_log_repo
from typing import Optional


async def log_audit_event(
    db: AsyncSession,
    action: str,
    user_id: Optional[str] = None,
    resource: Optional[str] = None,
    ip_address: Optional[str] = None,
):
    await audit_log_repo.create(
        db,
        obj_in={
            "action": action,
            "user_id": user_id,
            "resource": resource,
            "ip_address": ip_address,
        },
    )
