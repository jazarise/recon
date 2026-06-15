import pytest
import uuid
from core.db_manager import DatabaseManager
from database.schema.models import ScanModel, WorkflowRunModel

@pytest.fixture
def dbm():
    db_manager = DatabaseManager("pytest_stage6")
    yield db_manager
    db_manager.close()

def test_db_crud(dbm):
    session = dbm.get_session()
    sid = str(uuid.uuid4())
    s = ScanModel(id=sid, workflow="w1", target="t1", status="run")
    session.add(s)
    session.commit()
    
    loaded = session.query(ScanModel).filter_by(id=sid).first()
    assert loaded is not None
    assert loaded.target == "t1"
    
    loaded.status = "done"
    session.commit()
    
    assert session.query(ScanModel).filter_by(id=sid).first().status == "done"
    
    session.delete(loaded)
    session.commit()
    assert session.query(ScanModel).filter_by(id=sid).first() is None
    session.close()

def test_relationships(dbm):
    session = dbm.get_session()
    sid = str(uuid.uuid4())
    wid = str(uuid.uuid4())
    
    s = ScanModel(id=sid, workflow="w1", target="t1", status="run")
    w = WorkflowRunModel(id=wid, scan_id=sid, status="run")
    session.add(s)
    session.add(w)
    session.commit()
    
    loaded = session.query(ScanModel).filter_by(id=sid).first()
    assert len(loaded.workflow_runs) == 1
    session.close()
