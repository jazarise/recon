from reconx.core.database.repositories.base import BaseRepository
from reconx.core.database.models import Finding


class FindingRepository(BaseRepository[Finding]):
    pass


finding_repo = FindingRepository(Finding)
