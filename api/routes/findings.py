from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_findings():
    return [{"id": 1, "category": "vulnerability", "value": "XSS on api.example.com"}]
