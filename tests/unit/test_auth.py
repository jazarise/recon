import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from reconx.core.auth.auth_service import register_user, authenticate_user
from reconx.core.auth.jwt_manager import (
    create_access_token,
    verify_token,
    create_refresh_token,
)
from fastapi import HTTPException
from reconx.core.database.models import User


def test_jwt_manager():
    token = create_access_token("123", "admin")
    payload = verify_token(token)
    assert payload["sub"] == "123"
    assert payload["role"] == "admin"

    refresh = create_refresh_token("123")
    assert "token" in refresh
    assert "jti" in refresh


@pytest.mark.asyncio
async def test_register_user_weak_password():
    session = AsyncMock()
    with pytest.raises(HTTPException) as exc:
        await register_user(session, "test", "test@test.com", "weak", "127.0.0.1")
    assert exc.value.status_code == 400


@pytest.mark.asyncio
@patch("reconx.core.auth.auth_service.user_repo")
@patch("reconx.core.auth.auth_service.password_history_repo")
@patch("reconx.core.auth.auth_service.log_audit_event")
async def test_register_user_success(mock_audit, mock_hist, mock_user_repo):
    session = AsyncMock()
    mock_result = MagicMock()
    session.execute.return_value = mock_result
    mock_result.scalars.return_value.first.return_value = None

    mock_user_repo.create = AsyncMock(return_value=User(id="123", username="test"))
    mock_hist.create = AsyncMock()

    user = await register_user(
        session, "test", "test@test.com", "StrongPass123!", "127.0.0.1"
    )
    assert user.id == "123"
    assert mock_user_repo.create.called


@pytest.mark.asyncio
@patch("reconx.core.auth.auth_service.verify_password")
async def test_authenticate_user_invalid(mock_verify):
    session = AsyncMock()
    mock_result = MagicMock()
    session.execute.return_value = mock_result
    mock_result.scalars.return_value.all.return_value = []
    mock_result.scalars.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        await authenticate_user(session, "test", "pass", "127.0.0.1", "agent")
    assert exc.value.status_code == 401
