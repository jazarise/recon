from reconx.core.database.repositories.base import BaseRepository
from reconx.core.database.models import PasswordHistory


class PasswordHistoryRepository(BaseRepository[PasswordHistory]):
    pass


password_history_repo = PasswordHistoryRepository(PasswordHistory)
