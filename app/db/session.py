from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=True, # Показывает SQL-запросы в консоли
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    """Зависимость для FastAPI: отдает сессию и закрывает по окончании запроса."""
    async with async_session() as session:
        yield session