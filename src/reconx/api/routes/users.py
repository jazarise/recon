from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from reconx.core.database.session import get_db
from reconx.api.dependencies import get_current_user, require_admin
from reconx.schemas.core import UserRead
from reconx.core.database.models import User
from reconx.core.database.repositories.user import user_repo
from reconx.core.auth.auth_service import change_password
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/change-password")
async def update_password(
    req: ChangePasswordRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ip = request.client.host if request.client else "unknown"
    await change_password(db, current_user.id, req.old_password, req.new_password, ip)
    return {"message": "Password changed successfully"}


# Admin only endpoints
@router.get("", response_model=List[UserRead])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    return await user_repo.get_multi(db, skip=skip, limit=limit)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    user = await user_repo.delete(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
