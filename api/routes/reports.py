from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_reports():
    return [{"id": 1, "name": "Scan_Report_1"}]

@router.post("/")
def create_report(scan_id: str):
    return {"id": 2, "name": f"Scan_Report_{scan_id}"}
