from fastapi import APIRouter, Depends
from reconx.api.dependencies import require_admin
from reconx.core.database.models import User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
async def admin_dashboard(current_user: User = Depends(require_admin)):
    return {"message": "Welcome to the admin dashboard"}
