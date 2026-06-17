from reconx.core.database.repositories.base import BaseRepository
from reconx.core.database.models import Project


class ProjectRepository(BaseRepository[Project]):
    pass


project_repo = ProjectRepository(Project)
