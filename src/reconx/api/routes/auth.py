from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from reconx.core.database.session import get_db
from reconx.core.auth.auth_service import register_user, authenticate_user
from reconx.schemas.core import UserCreate, UserRead
from reconx.core.auth.refresh_tokens import is_token_revoked, revoke_refresh_token
from reconx.core.auth.jwt_manager import verify_token, create_access_token
from reconx.api.dependencies import get_current_user
from reconx.core.database.models import User
from reconx.core.audit.audit_service import log_audit_event
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenRefreshRequest(BaseModel):
    refresh_token: str


@router.post("/register", response_model=UserRead)
async def register(
    user_in: UserCreate, request: Request, db: AsyncSession = Depends(get_db)
):
    ip = request.client.host if request.client else "unknown"
    return await register_user(
        db, user_in.username, user_in.email, user_in.password, ip
    )


@router.post("/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    return await authenticate_user(
        db, form_data.username, form_data.password, ip, user_agent
    )


@router.post("/refresh")
async def refresh(refresh_req: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    try:
        payload = verify_token(refresh_req.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        jti = payload.get("jti")
        user_id = payload.get("sub")

        if not isinstance(jti, str) or not isinstance(user_id, str):
            raise HTTPException(status_code=401, detail="Invalid token payload")

        if await is_token_revoked(db, jti):
            raise HTTPException(status_code=401, detail="Token revoked")

        # Rotate refresh token (revoke old one)
        await revoke_refresh_token(db, jti)

        # In a full implementation, we'd issue a new refresh token here
        # but to keep it simple, we just return a new access token
        user_repo_module = __import__(
            "reconx.core.database.repositories.user", fromlist=["user_repo"]
        )
        user = await user_repo_module.user_repo.get(db, id=user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Invalid user")

        access_token = create_access_token(user.id, user.role)
        return {"access_token": access_token, "token_type": "bearer"}  # nosec B105
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Try to extract session ID from request headers or elsewhere if implemented
    # For now, just log the event
    ip = request.client.host if request.client else "unknown"
    await log_audit_event(db, action="Logout", user_id=current_user.id, ip_address=ip)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserRead)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
