from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from reconx.core.database.models import User, PasswordHistory, LoginAttempt
from reconx.core.database.repositories.user import user_repo
from reconx.core.database.repositories.password_history import password_history_repo
from reconx.core.database.repositories.login_attempt import login_attempt_repo
from reconx.core.auth.password_manager import (
    hash_password,
    verify_password,
    validate_password_strength,
)
from reconx.core.auth.jwt_manager import create_access_token, create_refresh_token
from reconx.core.auth.refresh_tokens import store_refresh_token
from reconx.core.auth.session_manager import create_session
from reconx.core.audit.audit_service import log_audit_event
from fastapi import HTTPException, status
from datetime import datetime, timezone, timedelta

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_MINUTES = 15
PASSWORD_HISTORY_LIMIT = 5


async def register_user(
    db: AsyncSession, username: str, email: str, plain_password: str, ip_address: str
) -> User:
    # Validate password first
    try:
        validate_password_strength(plain_password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Check if exists
    existing = await db.execute(
        select(User).filter((User.username == username) | (User.email == email))
    )
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    hashed = hash_password(plain_password)
    user = await user_repo.create(
        db,
        obj_in={
            "username": username,
            "email": email,
            "password_hash": hashed,
            "role": "viewer",  # default role
        },
    )

    # Store password history
    await password_history_repo.create(
        db, obj_in={"user_id": user.id, "password_hash": hashed}
    )

    await log_audit_event(
        db,
        action="User Creation",
        user_id=user.id,
        resource=username,
        ip_address=ip_address,
    )
    return user


async def authenticate_user(
    db: AsyncSession,
    username: str,
    plain_password: str,
    ip_address: str,
    user_agent: str,
) -> dict:
    # Rate Limiting Check
    lockout_threshold = datetime.now(timezone.utc) - timedelta(minutes=LOCKOUT_MINUTES)
    recent_attempts = await db.execute(
        select(LoginAttempt).filter(
            LoginAttempt.username == username,
            LoginAttempt.successful.is_(False),
            LoginAttempt.timestamp >= lockout_threshold,
        )
    )
    attempts = recent_attempts.scalars().all()
    if len(attempts) >= MAX_LOGIN_ATTEMPTS:
        await log_audit_event(
            db, action="Account Lockout", resource=username, ip_address=ip_address
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Account locked due to too many failed attempts",
        )

    # Find user
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()

    if not user or not verify_password(plain_password, user.password_hash):
        await login_attempt_repo.create(
            db,
            obj_in={
                "username": username,
                "ip_address": ip_address,
                "successful": False,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled"
        )

    await login_attempt_repo.create(
        db, obj_in={"username": username, "ip_address": ip_address, "successful": True}
    )
    await log_audit_event(db, action="Login", user_id=user.id, ip_address=ip_address)

    # Tokens
    access_token = create_access_token(user.id, user.role)
    refresh_data = create_refresh_token(user.id)

    await store_refresh_token(db, user.id, refresh_data["jti"], refresh_data["exp"])
    session = await create_session(db, user.id, ip_address, user_agent)

    return {
        "access_token": access_token,
        "refresh_token": refresh_data["token"],
        "token_type": "bearer",  # nosec B105
        "session_id": session.session_id,
    }


async def change_password(
    db: AsyncSession,
    user_id: str,
    old_password: str,
    new_password: str,
    ip_address: str,
):
    user = await user_repo.get(db, id=user_id)
    if not user or not verify_password(old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid current password"
        )

    try:
        validate_password_strength(new_password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Check history
    history_result = await db.execute(
        select(PasswordHistory)
        .filter(PasswordHistory.user_id == user_id)
        .order_by(PasswordHistory.created_at.desc())
        .limit(PASSWORD_HISTORY_LIMIT)
    )
    for hist in history_result.scalars().all():
        if verify_password(new_password, hist.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password has been used recently",
            )

    hashed = hash_password(new_password)
    await user_repo.update(db, db_obj=user, obj_in={"password_hash": hashed})

    await password_history_repo.create(
        db, obj_in={"user_id": user.id, "password_hash": hashed}
    )
    await log_audit_event(
        db, action="Password Change", user_id=user.id, ip_address=ip_address
    )
