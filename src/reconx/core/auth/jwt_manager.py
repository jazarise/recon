import jwt
from datetime import datetime, timedelta, timezone
from reconx.config.settings import settings
import uuid

ALGORITHM = "HS256"


def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {
        "sub": str(user_id),
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "jti": str(uuid.uuid4()),
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.security.jwt_secret, algorithm=ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(user_id: str) -> dict:
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    token_id = str(uuid.uuid4())
    to_encode = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "jti": token_id,
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.security.jwt_secret, algorithm=ALGORITHM
    )
    return {"token": encoded_jwt, "jti": token_id, "exp": expire}


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.security.jwt_secret, algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token is expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
