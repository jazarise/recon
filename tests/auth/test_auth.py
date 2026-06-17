import pytest
import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from reconx.core.database.base import BaseModel
from reconx.api.routes.auth import router as auth_router
from reconx.api.routes.users import router as users_router
from reconx.api.routes.admin import router as admin_router
from reconx.core.database.session import get_db
from httpx import AsyncClient, ASGITransport

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)

engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    async with SessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_register_and_login(async_client: AsyncClient):
    # Register
    res = await async_client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "StrongPassword123!",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["username"] == "testuser"
    assert data["role"] == "viewer"

    # Login
    res = await async_client.post(
        "/auth/login", data={"username": "testuser", "password": "StrongPassword123!"}
    )
    assert res.status_code == 200
    token_data = res.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data


@pytest.mark.asyncio
async def test_invalid_login(async_client: AsyncClient):
    # Login with no user
    res = await async_client.post(
        "/auth/login", data={"username": "nope", "password": "StrongPassword123!"}
    )
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_viewer_accessing_admin_route(async_client: AsyncClient):
    # Register
    await async_client.post(
        "/auth/register",
        json={
            "username": "vieweruser",
            "email": "view@test.com",
            "password": "StrongPassword123!",
        },
    )

    # Login
    login_res = await async_client.post(
        "/auth/login", data={"username": "vieweruser", "password": "StrongPassword123!"}
    )
    token = login_res.json()["access_token"]

    # Access Admin Route
    res = await async_client.get(
        "/admin/dashboard", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 403
    assert res.json()["detail"] == "Admin access required"


@pytest.mark.asyncio
async def test_refresh_token(async_client: AsyncClient):
    await async_client.post(
        "/auth/register",
        json={
            "username": "refresher",
            "email": "ref@test.com",
            "password": "StrongPassword123!",
        },
    )

    login_res = await async_client.post(
        "/auth/login", data={"username": "refresher", "password": "StrongPassword123!"}
    )
    refresh_token = login_res.json()["refresh_token"]

    # Use refresh token
    refresh_res = await async_client.post(
        "/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert refresh_res.status_code == 200
    assert "access_token" in refresh_res.json()

    # Try reusing same refresh token (it was revoked)
    refresh_res_2 = await async_client.post(
        "/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert refresh_res_2.status_code == 401
    assert "Token revoked" in refresh_res_2.json()["detail"]


@pytest.mark.asyncio
async def test_expired_jwt(async_client: AsyncClient):
    # This requires mocking the JWT expiration which is tricky without external libs,
    # but we can rely on our valid login to prove structure. We can manually create an expired token.
    from reconx.config.settings import settings
    import jwt
    import datetime

    # Craft expired token manually
    to_encode = {
        "sub": "user_id",
        "role": "viewer",
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        - datetime.timedelta(seconds=1),
        "jti": "foo",
    }
    encoded_jwt = jwt.encode(to_encode, settings.security.jwt_secret, algorithm="HS256")

    res = await async_client.get(
        "/auth/me", headers={"Authorization": f"Bearer {encoded_jwt}"}
    )
    assert res.status_code == 401
    assert "expired" in res.json()["detail"].lower()
