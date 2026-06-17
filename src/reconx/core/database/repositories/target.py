from reconx.core.database.repositories.base import BaseRepository
from reconx.core.database.models import Target


class TargetRepository(BaseRepository[Target]):
    pass


target_repo = TargetRepository(Target)
