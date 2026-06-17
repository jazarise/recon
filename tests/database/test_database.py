import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from reconx.core.database.base import BaseModel
from reconx.core.database.models import Target, SeverityEnum, Finding
from reconx.core.database.repositories.user import user_repo
from reconx.core.database.repositories.project import project_repo
from reconx.core.database.repositories.scan import scan_repo


# Setup an in-memory SQLite for testing
@pytest_asyncio.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    Session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with Session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
    await engine.dispose()


@pytest.mark.asyncio
async def test_connection(test_db: AsyncSession):
    # If the fixture yields, the connection is good
    assert test_db is not None


@pytest.mark.asyncio
async def test_user_crud(test_db: AsyncSession):
    # Create user
    user = await user_repo.create(
        test_db,
        obj_in={
            "username": "test_user",
            "email": "test@example.com",
            "password_hash": "hash",
        },
    )
    assert user.id is not None
    assert user.username == "test_user"

    # Read user
    fetched = await user_repo.get(test_db, id=user.id)
    assert fetched is not None
    assert fetched.email == "test@example.com"

    # Update user
    await user_repo.update(test_db, db_obj=fetched, obj_in={"role": "admin"})
    assert fetched.role == "admin"

    # Delete user
    await user_repo.delete(test_db, id=user.id)
    assert await user_repo.get(test_db, id=user.id) is None


@pytest.mark.asyncio
async def test_project_crud(test_db: AsyncSession):
    user = await user_repo.create(
        test_db,
        obj_in={
            "username": "owner",
            "email": "owner@example.com",
            "password_hash": "hash",
        },
    )

    # Create project
    project = await project_repo.create(
        test_db, obj_in={"name": "Project X", "owner_id": user.id}
    )
    assert project.id is not None

    # Delete project
    await project_repo.delete(test_db, id=project.id)
    assert await project_repo.get(test_db, id=project.id) is None


@pytest.mark.asyncio
async def test_scan_crud(test_db: AsyncSession):
    user = await user_repo.create(
        test_db,
        obj_in={"username": "scan", "email": "s@e.com", "password_hash": "hash"},
    )
    project = await project_repo.create(
        test_db, obj_in={"name": "Proj", "owner_id": user.id}
    )
    target = Target(project_id=project.id, target="127.0.0.1", target_type="ip")
    test_db.add(target)
    await test_db.commit()
    await test_db.refresh(target)

    # Create scan
    scan = await scan_repo.create(
        test_db,
        obj_in={"project_id": project.id, "target_id": target.id, "scan_type": "nmap"},
    )
    assert scan.id is not None

    # Store results (finding)
    finding = Finding(
        scan_id=scan.id,
        severity=SeverityEnum.critical,
        title="SQLi",
        description="Found SQLi",
    )
    test_db.add(finding)
    await test_db.commit()
    await test_db.refresh(finding)

    assert finding.id is not None
    assert finding.scan_id == scan.id
