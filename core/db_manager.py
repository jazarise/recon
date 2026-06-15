from core.paths import BASE_DIR

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from database.schema.models import Base


class DatabaseManager:
    """Manages SQLite database connections per project workspace."""
    
    def __init__(self, project_name: str = "default"):
        self.project_name = project_name
        
        # Ensure project directory exists
        self.project_dir = BASE_DIR / "projects" / project_name
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        # SQLite database path
        self.db_path = self.project_dir / "reconx.db"
        
        # Setup SQLAlchemy with WAL mode for better concurrency
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            connect_args={"check_same_thread": False},
            pool_pre_ping=True,
        )

        # Enable WAL journal mode for reduced locking
        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA busy_timeout=5000")
            cursor.close()

        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    def close(self):
        """Dispose engine and release all file handles (critical on Windows)."""
        self.engine.dispose()
