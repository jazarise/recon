from fastapi import APIRouter
from api.schemas.common import StandardResponse

router = APIRouter()

@router.get("/", response_model=StandardResponse)
def get_reports():
    return StandardResponse(success=True, message="Reports retrieved", data={"reports": []})
