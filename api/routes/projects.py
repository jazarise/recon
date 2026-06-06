from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_projects():
    return [{"id": 1, "name": "Default Project"}]

@router.post("/")
def create_project(name: str):
    return {"id": 2, "name": name}
