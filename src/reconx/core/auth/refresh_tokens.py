from sqlalchemy.ext.asyncio import AsyncSession
from reconx.core.database.repositories.refresh_token import refresh_token_repo
from reconx.core.database.models import RefreshToken


async def store_refresh_token(
    db: AsyncSession, user_id: str, token_id: str, expires_at
) -> RefreshToken:
    return await refresh_token_repo.create(
        db,
        obj_in={
            "token_id": token_id,
            "user_id": user_id,
            "expires_at": expires_at,
            "revoked": False,
        },
    )


async def revoke_refresh_token(db: AsyncSession, token_id: str):
    # This requires looking up by token_id which is not the primary key, so we need a custom query
    from sqlalchemy import select

    result = await db.execute(
        select(RefreshToken).filter(RefreshToken.token_id == token_id)
    )
    token_record = result.scalars().first()
    if token_record:
        await refresh_token_repo.update(
            db, db_obj=token_record, obj_in={"revoked": True}
        )


async def is_token_revoked(db: AsyncSession, token_id: str) -> bool:
    from sqlalchemy import select

    result = await db.execute(
        select(RefreshToken).filter(RefreshToken.token_id == token_id)
    )
    token_record = result.scalars().first()
    if not token_record:
        return True  # Treat unknown as revoked
    return token_record.revoked
