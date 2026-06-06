from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_assets():
    return [{"id": 1, "value": "example.com"}]

@router.post("/")
def create_asset(value: str):
    return {"id": 2, "value": value}
