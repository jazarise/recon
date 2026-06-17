from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from reconx.config.settings import settings

engine = create_async_engine(
    settings.database.url, echo=settings.app.debug, future=True
)

async_session_factory = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db():
    async with async_session_factory() as session:
        yield session
