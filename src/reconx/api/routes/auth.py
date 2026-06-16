from fastapi import APIRouter
from reconx.api.schemas.common import StandardResponse

router = APIRouter()

@router.post("/login", response_model=StandardResponse)
def login():
    return StandardResponse(success=True, message="Login successful", data={"token": "mock_token"})
