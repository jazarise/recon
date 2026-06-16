from fastapi import APIRouter
from reconx.api.schemas.common import StandardResponse

router = APIRouter()

@router.get("/", response_model=StandardResponse)
def get_findings():
    return StandardResponse(success=True, message="Findings retrieved", data={"findings": []})
