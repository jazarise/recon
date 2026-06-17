from reconx.core.database.repositories.base import BaseRepository
from reconx.core.database.models import Scan


class ScanRepository(BaseRepository[Scan]):
    pass


scan_repo = ScanRepository(Scan)
