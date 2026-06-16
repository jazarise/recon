from fastapi import APIRouter
from reconx.api.schemas.common import StandardResponse

router = APIRouter()

@router.get("/", response_model=StandardResponse)
def get_assets():
    return StandardResponse(success=True, message="Assets retrieved", data={"assets": []})
