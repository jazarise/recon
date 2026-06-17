from reconx.core.database.repositories.base import BaseRepository
from reconx.core.database.models import RefreshToken


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    pass


refresh_token_repo = RefreshTokenRepository(RefreshToken)
