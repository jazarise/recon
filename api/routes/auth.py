from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login(username: str):
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}
