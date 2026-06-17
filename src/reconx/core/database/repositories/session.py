from reconx.core.database.repositories.base import BaseRepository
from reconx.core.database.models import Session


class SessionRepository(BaseRepository[Session]):
    pass


session_repo = SessionRepository(Session)
