import uuid
import asyncio
from fastapi import APIRouter, Depends, HTTPException
from reconx.core.orchestrator import orchestrator
from reconx.core.db_manager import DatabaseManager
from reconx.database.schema.models import ScanModel
from reconx.api.schemas.common import StandardResponse, ScanRequest

router = APIRouter()

# Dependency to get db session
def get_db_session():
    db = DatabaseManager()
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()

@router.get("/", response_model=StandardResponse)
def get_scans(session = Depends(get_db_session)):
    scans = session.query(ScanModel).all()
    scan_list = [{"id": s.id, "target": s.target, "workflow": s.workflow, "status": s.status} for s in scans]
    return StandardResponse(success=True, message="Scans retrieved", data={"scans": scan_list})

@router.post("/", response_model=StandardResponse)
async def create_scan(request: ScanRequest, session = Depends(get_db_session)):
    scan_id = str(uuid.uuid4())
    scan = ScanModel(
        id=scan_id,
        workflow=request.workflow,
        target=request.target,
        status="running"
    )
    session.add(scan)
    session.commit()
    
    # Fire orchestrator task in background
    asyncio.create_task(orchestrator.run_workflow(request.workflow, request.target))
    
    return StandardResponse(
        success=True,
        message="Scan started successfully",
        data={"scan_id": scan_id, "target": request.target, "workflow": request.workflow}
    )

@router.get("/{scan_id}", response_model=StandardResponse)
def get_scan(scan_id: str, session = Depends(get_db_session)):
    scan = session.query(ScanModel).filter(ScanModel.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return StandardResponse(
        success=True,
        message="Scan retrieved",
        data={"id": scan.id, "target": scan.target, "status": scan.status, "workflow": scan.workflow}
    )
