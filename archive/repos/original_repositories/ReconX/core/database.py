from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from core.models import Base
from core.paths import PROJECT_ROOT

class DatabaseManager:
    """Manages SQLite database connections per project workspace."""
    
    def __init__(self, project_name: str = "default"):
        self.project_name = project_name
        
        # Ensure project directory exists
        self.project_dir = PROJECT_ROOT / "projects" / project_name
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        # SQLite database path
        self.db_path = self.project_dir / "reconx.db"
        
        # Setup SQLAlchemy
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()
