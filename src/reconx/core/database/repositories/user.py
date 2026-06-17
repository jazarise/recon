from reconx.core.database.repositories.base import BaseRepository
from reconx.core.database.models import User


class UserRepository(BaseRepository[User]):
    pass


user_repo = UserRepository(User)
