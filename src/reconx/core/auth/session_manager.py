from sqlalchemy.ext.asyncio import AsyncSession
from reconx.core.database.repositories.session import session_repo
from reconx.core.database.models import Session
from datetime import datetime, timezone
import uuid
from sqlalchemy import select


async def create_session(
    db: AsyncSession, user_id: str, ip_address: str, user_agent: str
) -> Session:
    return await session_repo.create(
        db,
        obj_in={
            "user_id": user_id,
            "session_id": str(uuid.uuid4()),
            "ip_address": ip_address,
            "user_agent": user_agent,
            "is_active": True,
        },
    )


async def terminate_session(db: AsyncSession, session_id: str):
    result = await db.execute(select(Session).filter(Session.session_id == session_id))
    session_record = result.scalars().first()
    if session_record:
        await session_repo.update(
            db,
            db_obj=session_record,
            obj_in={"is_active": False, "logout_time": datetime.now(timezone.utc)},
        )


async def terminate_all_sessions(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(Session).filter(Session.user_id == user_id, Session.is_active.is_(True))
    )
    sessions = result.scalars().all()
    for session_record in sessions:
        await session_repo.update(
            db,
            db_obj=session_record,
            obj_in={"is_active": False, "logout_time": datetime.now(timezone.utc)},
        )
