from reconx.core.database.repositories.base import BaseRepository
from reconx.core.database.models import LoginAttempt


class LoginAttemptRepository(BaseRepository[LoginAttempt]):
    pass


login_attempt_repo = LoginAttemptRepository(LoginAttempt)
