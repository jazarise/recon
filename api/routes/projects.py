from fastapi import APIRouter
from api.schemas.common import StandardResponse

router = APIRouter()

@router.get("/", response_model=StandardResponse)
def get_projects():
    return StandardResponse(success=True, message="Projects retrieved", data={"projects": []})
