import pytest
from unittest.mock import AsyncMock, MagicMock
from reconx.core.database.repositories.user import UserRepository
from reconx.core.database.repositories.project import ProjectRepository
from reconx.core.database.repositories.finding import FindingRepository
from reconx.core.database.repositories.scan import ScanRepository
from reconx.core.database.repositories.target import TargetRepository
from reconx.core.database.models import User, Project, Finding, Scan, Target


@pytest.mark.asyncio
async def test_user_repository():
    session = AsyncMock()
    mock_result = MagicMock()
    session.execute.return_value = mock_result
    mock_result.scalars.return_value.first.return_value = User(
        id="123", username="test"
    )

    repo = UserRepository(User)
    user = await repo.get(session, id="123")
    assert user is not None
    assert user.id == "123"


@pytest.mark.asyncio
async def test_project_repository():
    session = AsyncMock()
    mock_result = MagicMock()
    session.execute.return_value = mock_result
    mock_result.scalars.return_value.all.return_value = [Project(id="1", name="Proj")]

    repo = ProjectRepository(Project)
    projects = await repo.get_multi(session)
    assert len(projects) == 1


@pytest.mark.asyncio
async def test_finding_repository():
    session = AsyncMock()
    mock_result = MagicMock()
    session.execute.return_value = mock_result
    mock_result.scalars.return_value.all.return_value = []

    repo = FindingRepository(Finding)
    findings = await repo.get_multi(session)
    assert isinstance(findings, list)
    assert len(findings) == 0


@pytest.mark.asyncio
async def test_scan_repository():
    session = AsyncMock()
    mock_result = MagicMock()
    session.execute.return_value = mock_result
    mock_result.scalars.return_value.first.return_value = Scan(
        id="1", status="COMPLETED"
    )

    repo = ScanRepository(Scan)
    scan = await repo.get(session, id="1")
    assert scan is not None
    assert scan.status == "COMPLETED"


@pytest.mark.asyncio
async def test_target_repository():
    session = AsyncMock()
    mock_result = MagicMock()
    session.execute.return_value = mock_result
    mock_result.scalars.return_value.all.return_value = [Target(id="1")]

    repo = TargetRepository(Target)
    targets = await repo.get_multi(session)
    assert len(targets) == 1
